package token;

import java.util.Date;
import java.util.UUID;

import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.DecodedJWT;

import static java.lang.String.format;
import static servlets.ApiServlet.ACCESS_TOKEN_HEADER;

public class TokenUtils {
    private final String privateKey;

    public TokenUtils(String privateKey) {
        this.privateKey = privateKey;
    }

    public TokensResponse generateTokens(long userId) {
        return new TokensResponse(generateAccessToken(userId), generateRefreshToken());
    }

    public String generateAccessToken(long userId) {
        Algorithm algorithm = Algorithm.HMAC256(privateKey);
        return JWT.create()
            .withClaim("user_id", userId)
            .withIssuer("mix-application-main-server")
            .withExpiresAt(new Date(System.currentTimeMillis() + (365L * 24 * 60 * 60 * 1000)))
            .withIssuedAt(new Date(System.currentTimeMillis()))
            .sign(algorithm);
    }

    public String generateRefreshToken() {
        return UUID.randomUUID().toString();
    }

    public DecodedJWT verifyAccessToken(String accessToken) throws TokenMatchingException {
        if (accessToken == null) {
            throw new TokenMatchingException(format("Access token was not found in %s header", ACCESS_TOKEN_HEADER));
        }
        if (accessToken.isEmpty()) {
            throw new TokenMatchingException(format("Access token is empty in %s header", ACCESS_TOKEN_HEADER));
        }
        Algorithm algorithm = Algorithm.HMAC256(privateKey);
        JWTVerifier verifier = JWT.require(algorithm)
            .withIssuer("mix-application-main-server")
            .build(); //Reusable verifier instance
        return verifier.verify(accessToken);
    }
}
