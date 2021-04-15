package token;

public class TokenMatchingException extends Exception {
    public TokenMatchingException(String message) {
        super(message);
    }
    TokenMatchingException(String message, Throwable throwable) {
        super(message, throwable);
    }
}
