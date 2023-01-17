(defvar *ip-addr* nil)
(defvar *ssid* "YOUR-SSID")
(defvar *passwd* "YOUR-PASS")

(defun println (x s)
  (princ x s)
  (princ #\return s)
  (princ #\newline s))

(defun start-wifi ()
  (princ "Connecting to wifi...")
  (terpri)
  (setq *ip-addr* (wifi-connect *ssid* *passwd*))
  (princ "Connected! IP: ")
  (princ *ip-addr*)
  (terpri))

(defun respond (stream &optional body)
  (cond ((or (stringp body)
             (null body))
         (println "HTTP/1.1 200 OK" stream))
        (t (println "HTTP/1.1 404 Not Found" stream)))
  (when (stringp body)
    (println "Content-Type: application/json" stream))
  (println "Connection: close" stream)
  (println "" stream)
  (when (stringp body)
    (println body stream)
    (println "" stream)))

(defun request-dispatch (request stream)
  (cond
    ((string= request "POST /led/off ")
     (digitalwrite :led-builtin nil)
     (respond stream))
    ((string= request "POST /led/on ")
     (digitalwrite :led-builtin t)
     (respond stream))
    ((string= request "GET / ")
     (respond
      stream
      "{\"message\": \"Hello world!\"}"))
    (t (respond stream t))))

(defun run-rest-server ()
  (princ "Starting server...")
  (terpri)
  (loop
    (with-client (stream)
      (let ((request (read-line stream)))
        (loop
          (unless (read-line stream)
            (return)))
        (request-dispatch
         (subseq
          request
          0
          (- (length request) 1 8))
         stream)))
    (delay 16)))


(start-wifi)
(wifi-server)
(run-rest-server)
