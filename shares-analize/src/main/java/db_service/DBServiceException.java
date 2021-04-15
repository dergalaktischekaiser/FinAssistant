package db_service;

public class DBServiceException extends Exception{
    public DBServiceException(String message) {
        super(message);
    }
    public DBServiceException(String message, Throwable throwable) {
        super(message, throwable);
    }
}
