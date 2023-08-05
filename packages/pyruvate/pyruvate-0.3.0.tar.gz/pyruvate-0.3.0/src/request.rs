use bytes::{Bytes, BytesMut};
use httparse::{self};
use log::{debug};
use cpython::exc::{UnicodeDecodeError, ValueError};
use cpython::{PyErr, PyResult, Python};
use std::net::SocketAddr;
use urlencoding::{decode};


// https://tools.ietf.org/html/rfc7230#section-3.2
// Each header field consists of a case-insensitive field name ...
pub const CONTENT_LENGTH_HEADER: &str = "content-length";
const CONTENT_TYPE_HEADER: &str = "content-type";
const CONTENT_TYPE: &str = "CONTENT_TYPE";
const REQUEST_METHOD: &str = "REQUEST_METHOD";
const PATH_INFO: &str = "PATH_INFO";
const QUERY_STRING: &str = "QUERY_STRING";
const SERVER_PROTOCOL: &str = "SERVER_PROTOCOL";


macro_rules! environ_set {
    ($self:expr, $key:ident, $header:expr, $py:expr) => {
        match String::from_utf8($header.value.to_vec()) {
            Ok(val) => $self.environ.push(($key.to_string(), val)),
            Err(e) => return Err(PyErr::new::<UnicodeDecodeError, _>($py, format!("{:?} encountered for value: {:?}", e, $header.value)))
        }
    }
}


pub struct WSGIRequest {
    pub body: BytesMut,
    pub complete: bool,
    pub content_length: usize,
    pub environ: Vec<(String, String)>,
    pub peer_addr: Option<SocketAddr>,
    }


impl WSGIRequest {

    pub fn new(peer_addr: Option<SocketAddr>) -> WSGIRequest {
        WSGIRequest {
            body: BytesMut::new(),
            complete: false,
            content_length: 0,
            environ: Vec::new(),
            peer_addr,
        }
    }

    pub fn parse(&mut self, raw: Bytes, py: Python) -> PyResult<()> {
        if !self.complete {
            if self.environ.is_empty() {
                return self.parse_headers(raw, py)
            }
            if self.content_length == (self.body.len() + raw.len()) {
                self.complete = true;
            }
            self.body.extend_from_slice(&raw[..]);
        }
        Ok(())
    }

    pub fn parse_headers(&mut self, raw: Bytes, py: Python) -> PyResult<()> {
        let mut headers = [httparse::EMPTY_HEADER; 16];
        let mut req = httparse::Request::new(&mut headers);
        match req.parse(&raw[..]) {
            Ok(res) => {
                match res {
                    httparse::Status::Partial => {
                        debug!("Partial request");
                    },
                    httparse::Status::Complete(size) => {
                        let length = raw.len();
                        if size < length {
                            self.body.extend_from_slice(&raw[size..length]);
                        } else {
                            self.complete = true;
                        }
                        for header in req.headers.iter() {
                            match header.name.to_lowercase().as_str() {
                                CONTENT_LENGTH_HEADER => {
                                    if let Ok(val) = std::str::from_utf8(header.value) {
                                        if let Ok(parsedval) = val.parse() {
                                            self.content_length = parsedval;
                                            if self.content_length == self.body.len() {
                                                self.complete = true;
                                            }
                                        }
                                    }
                                },
                                CONTENT_TYPE_HEADER => {
                                    environ_set!(self, CONTENT_TYPE, header, py);
                                },
                                &_ => {
                                    match String::from_utf8(header.value.to_vec()) {
                                        Ok(val) => {
                                            let mut key = "HTTP_".to_string();
                                            key.push_str(&header.name.to_ascii_uppercase().replace("-", "_"));
                                            self.environ.push((key, val))
                                        },
                                        Err(e) => return Err(PyErr::new::<UnicodeDecodeError, _>(py, format!("{:?} encountered for value: {:?}", e, header.value)))
                                    }
                                }
                            }
                        }
                        if let Some(method) = req.method {
                            self.environ.push((REQUEST_METHOD.to_string(), method.to_string()));
                        }
                        if let Some(path) = req.path {
                            match decode(path) {
                                Ok(decoded) => {
                                    let parts: Vec<&str> = decoded.split('?').collect();
                                    self.environ.push((PATH_INFO.to_string(), parts[0].to_string()));
                                    if parts.len() > 1 {
                                        self.environ.push((QUERY_STRING.to_string(), parts[1].to_string()));
                                    } else {
                                        self.environ.push((QUERY_STRING.to_string(), "".to_string()));
                                    }
                                },
                                Err(e) => return Err(PyErr::new::<ValueError, _>(py, format!("Could not urldecode path info: {:?}", e)))
                            }
                        }
                        if let Some(version) = req.version {
                            let protocol = match version {
                                0 => "HTTP/1.0",
                                1 => "HTTP/1.1",
                                _ => return Err(PyErr::new::<ValueError, _>(py, format!("Unsupported version: {:?}", version)))
                            };
                            self.environ.push((SERVER_PROTOCOL.to_string(), protocol.to_string()));
                        }
                    }
                }
            },
            Err(err) => return Err(PyErr::new::<ValueError, _>(py, format!("Error parsing request: {:?}", err)))
        };
        Ok(())
    }

}

#[cfg(test)]
mod tests {
    use bytes::{Bytes};
    use log::{debug};
    use cpython::{Python};

    use crate::request::{WSGIRequest};

    #[test]
    fn test_get() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let raw = Bytes::from(&b"GET /foo42?bar=baz HTTP/1.1\r\nAuthorization: Basic YWRtaW46YWRtaW4=\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n"[..]);
        let mut got = WSGIRequest::new(None);
        got.parse_headers(raw, py).unwrap();
        assert!(got.environ.len() == 13);
        for (name, value) in got.environ.iter() {
            match name.as_str() {
                "HTTP_COOKIE" => assert!(&value[..] == "foo_language=en;"),
                "PATH_INFO" => assert!(&value[..] == "/foo42"),
                "QUERY_STRING" => assert!(&value[..] == "bar=baz"),
                "HTTP_ACCEPT" => assert!(&value[..] == "image/webp,*/*"),
                "HTTP_ACCEPT_LANGUAGE" => assert!(&value[..] == "de-DE,en-US;q=0.7,en;q=0.3"),
                "HTTP_ACCEPT_ENCODING" => assert!(&value[..] == "gzip, deflate"),
                "HTTP_AUTHORIZATION" => assert!(&value[..] == "Basic YWRtaW46YWRtaW4="),
                "HTTP_CONNECTION" => assert!(&value[..] == "keep-alive"),
                "REQUEST_METHOD" => assert!(&value[..] == "GET"),
                "HTTP_HOST" => assert!(&value[..] == "localhost:7878"),
                "HTTP_USER_AGENT" => {
                    let expected = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0";
                    assert_eq!(value, expected);
                },
                "HTTP_DNT" => assert_eq!(&value[..], "1"),
                "SERVER_PROTOCOL" => assert_eq!(&value[..], "HTTP/1.1"),
                &_ => {}
            }
        }
    }

    #[test]
    fn test_url_decode() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let raw = Bytes::from(&b"GET /foo%2042?bar=baz%20foo HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n"[..]);
        let mut got = WSGIRequest::new(None);
        got.parse_headers(raw, py).unwrap();
        assert!(got.environ.len() == 12);
        for (name, value) in got.environ.iter() {
            match name.as_str() {
                "HTTP_COOKIE" => assert!(&value[..] == "foo_language=en;"),
                "PATH_INFO" => assert!(&value[..] == "/foo 42"),
                "QUERY_STRING" => assert!(&value[..] == "bar=baz foo"),
                "HTTP_ACCEPT" => assert!(&value[..] == "image/webp,*/*"),
                "HTTP_ACCEPT_LANGUAGE" => assert!(&value[..] == "de-DE,en-US;q=0.7,en;q=0.3"),
                "HTTP_ACCEPT_ENCODING" => assert!(&value[..] == "gzip, deflate"),
                "HTTP_AUTHORIZATION" => assert!(&value[..] == "Basic YWRtaW46YWRtaW4="),
                "HTTP_CONNECTION" => assert!(&value[..] == "keep-alive"),
                "REQUEST_METHOD" => assert!(&value[..] == "GET"),
                "HTTP_HOST" => assert!(&value[..] == "localhost:7878"),
                "HTTP_USER_AGENT" => {
                    let expected = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0";
                    assert_eq!(value, expected);
                },
                "HTTP_DNT" => assert_eq!(&value[..], "1"),
                "SERVER_PROTOCOL" => assert_eq!(&value[..], "HTTP/1.1"),
                &_ => {}
            }
        }
    }

    #[test]
    fn test_error_url() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let raw = Bytes::from(&b"GET /foo 42?bar=baz foo HTTP/1.1\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n"[..]);
        let mut got = WSGIRequest::new(None);
        match got.parse_headers(raw, py) {
            Ok(_) => assert!(false),
            Err(e) => {
                e.print_and_set_sys_last_vars(py);
            }
        }
    }

    #[test]
    fn test_parse_body_once() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let raw = Bytes::from(&b"POST /test HTTP/1.1\r\nHost: foo.example\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 27\r\n\r\nfield1=value1&field2=value2"[..]);
        let mut got = WSGIRequest::new(None);
        got.parse(raw, py).expect("Error parsing request");
        assert!(got.complete);
        for (name, value) in got.environ.iter() {
            match name.as_str() {
                "CONTENT_TYPE" => {
                    let expected = "application/x-www-form-urlencoded";
                    assert_eq!(value, expected);
                },
                &_ => {}
            }
        }
        assert_eq!(&got.body[..], b"field1=value1&field2=value2");
    }

    #[test]
    fn test_parse_multiple() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let raw1 = Bytes::from(&b"POST /test HTTP/1.1\r\nHost: foo.example\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 41\r\n\r\nfield1=value1&field2=value2"[..]);
        let raw2 = Bytes::from(&b"&field3=value3"[..]);
        let mut got = WSGIRequest::new(None);
        got.parse(raw1, py).expect("Error parsing request");
        assert!(!got.complete);
        assert!(got.content_length == 41);
        got.parse(raw2, py).expect("Error parsing request");
        assert!(got.complete);
        assert!(got.content_length == 41);
        for (name, value) in got.environ.iter() {
            match name.as_str() {
                "CONTENT_TYPE" => {
                    let expected = "application/x-www-form-urlencoded";
                    assert_eq!(expected, value);
                },
                &_ => {}
            }
        }
        let expected = b"field1=value1&field2=value2&field3=value3";
        debug!("{:?}", got.body);
        assert!(
            got.body.iter().zip(expected.iter()).all(|(p,q)| p == q));
    }

}
