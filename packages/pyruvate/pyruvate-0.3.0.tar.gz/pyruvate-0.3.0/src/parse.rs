use log::{debug};
use cpython::{NoArgs, ObjectProtocol, PyBytes, PyClone, PyDict, PyResult, PyString, Python, PythonObject, PyTuple, ToPyObject};

use crate::globals::{WSGIGlobals};
use crate::request::{WSGIRequest};


pub fn get_environ(req: &WSGIRequest, globals: &WSGIGlobals, py: Python) -> PyResult<PyDict> {
    let io = &globals.io_module;
    let sys = &globals.sys_module;
    let environ = PyDict::new(py);
    for (k, v) in req.environ.iter() {
        environ.set_item(py, k, PyString::new(py, v))?;
    }
    environ.set_item(py, "SERVER_NAME", format!("{}", globals.server_info.ip()))?;
    environ.set_item(py, "SERVER_PORT", format!("{}", globals.server_info.port()))?;
    // XXX the following item needs to be set properly
    environ.set_item(py, "SCRIPT_NAME", "")?;
    environ.set_item(py, "REMOTE_ADDR", match req.peer_addr {
        None => "".to_string(),
        Some(addr) => format!("{}", addr.ip())
    })?;
    let input = io.call(py, "BytesIO", NoArgs, None)?;
    let bodylen = req.body.len();
    if bodylen > 0 {
        environ.set_item(py, "CONTENT_LENGTH", bodylen)?;
        input.call_method(py, "write", PyTuple::new(py, &[PyBytes::new(py, &req.body[..]).as_object().clone_ref(py)]), None)?;
        input.call_method(py, "seek", PyTuple::new(py, &[(0 as i32).to_py_object(py).as_object().clone_ref(py)]), None)?;
    }
    environ.set_item(py, "wsgi.input", input)?;
    environ.set_item(py, "wsgi.errors", sys.get(py, "stderr")?)?;
    environ.set_item(py, "wsgi.version", (1, 0))?;
    environ.set_item(py, "wsgi.multithread", false)?;
    environ.set_item(py, "wsgi.multiprocess", true)?;
    environ.set_item(py, "wsgi.run_once", false)?;
    environ.set_item(py, "wsgi.url_scheme", "http")?;
    if let Some(wsgi) = &globals.wsgi_module {
        debug!("Setting FileWrapper in environ");
        environ.set_item(py, "wsgi.file_wrapper", wsgi.get(py, "FileWrapper")?)?;
    }
    Ok(environ)
}

#[cfg(test)]
mod tests {
    use bytes::{Bytes};
    use log::{debug};
    use cpython::{NoArgs, ObjectProtocol, PyClone, Python, PythonObject, PyString, PyBytes};
    use std::net::SocketAddr;

    use crate::globals::{WSGIGlobals};
    use crate::parse::{get_environ};
    use crate::request::{WSGIRequest};

    macro_rules! assert_header {
        ($got:ident, $py:ident, $key:literal, $value:expr) => {
            assert!($got.get_item($py, $key).unwrap().extract::<PyString>($py).unwrap().to_string($py).unwrap() == $value);
        }
    }

    #[test]
    fn test_environ_dict() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let si = "127.0.0.1:7878".parse().unwrap();
        let sn = "/foo";
        let g = WSGIGlobals::new(si, sn, py);
        let raw = Bytes::from(&b"GET /foo42?bar=baz HTTP/1.1\r\nAuthorization: Basic YWRtaW46YWRtaW4=\r\nHost: localhost:7878\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0\r\nAccept: image/webp,*/*\r\nAccept-Language: de-DE,en-US;q=0.7,en;q=0.3\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\nCookie: foo_language=en;\r\nDNT: 1\r\n\r\n"[..]);
        let mut req = WSGIRequest::new(Some(SocketAddr::new("192.168.1.23".parse().unwrap(), 43567)));
        req.parse(raw, py).expect("Error parsing request");
        let got = get_environ(&req, &g, py).unwrap();
        assert_header!(got, py, "SERVER_NAME", "127.0.0.1");
        assert_header!(got, py, "SERVER_PORT", "7878");
        assert_header!(got, py, "SCRIPT_NAME", "");
        assert_header!(got, py, "REMOTE_ADDR", "192.168.1.23");
        assert_header!(got, py, "HTTP_COOKIE", "foo_language=en;");
        assert_header!(got, py, "PATH_INFO", "/foo42");
        assert_header!(got, py, "QUERY_STRING", "bar=baz");
        assert_header!(got, py, "HTTP_ACCEPT", "image/webp,*/*");
        assert_header!(got, py, "HTTP_ACCEPT_LANGUAGE", "de-DE,en-US;q=0.7,en;q=0.3");
        assert_header!(got, py, "HTTP_ACCEPT_ENCODING", "gzip, deflate");
        assert_header!(got, py, "HTTP_AUTHORIZATION", "Basic YWRtaW46YWRtaW4=");
        assert_header!(got, py, "HTTP_CONNECTION", "keep-alive");
        assert_header!(got, py, "REQUEST_METHOD", "GET");
        assert_header!(got, py, "HTTP_HOST", "localhost:7878");
        assert_header!(got, py, "HTTP_USER_AGENT", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0");
        assert_header!(got, py, "HTTP_DNT", "1");
        assert_header!(got, py, "SERVER_PROTOCOL", "HTTP/1.1");
    }

    #[test]
    fn test_post_simple_form() {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let si = "127.0.0.1:7878".parse().unwrap();
        let sn = "/foo";
        let g = WSGIGlobals::new(si, sn, py);
        let raw = Bytes::from(&b"POST /test HTTP/1.1\r\nHost: foo.example\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 27\r\n\r\nfield1=value1&field2=value2"[..]);
        let mut req = WSGIRequest::new(None);
        req.parse(raw, py).expect("Error parsing request");
        let got = get_environ(&req, &g, py).unwrap();
        assert_header!(got, py, "CONTENT_TYPE", "application/x-www-form-urlencoded");
        let input = got.get_item(py, "wsgi.input").unwrap().as_object().clone_ref(py);
        debug!("{:?}", input);
        let input = input.call_method(py, "read", NoArgs, None).unwrap();
        debug!("{:?}", input);
        assert!(input.extract::<PyBytes>(py).unwrap().data(py) == b"field1=value1&field2=value2");
    }

}
