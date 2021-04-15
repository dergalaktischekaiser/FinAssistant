package authorization.apple;

import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * The response token object returned on a successful request.
 */
public final class AppleTokenResponse {
    /**
     * A JSON Web Token that contains the user’s identity information.
     */
    private final String idToken;

    /**
     * (Reserved for future use) A token used to access allowed data. Currently, no data set has been defined for access.
     */
    private final String accessToken;

    /**
     * The type of access token. It will always be bearer.
     */
    private final String tokenType;

    /**
     * The amount of time, in seconds, before the access token expires.
     */
    private final Long expiresIn;

    /**
     * The refresh token used to regenerate new access tokens. Store this token securely on your server.
     */
    private final String refreshToken;

    public AppleTokenResponse(@JsonProperty("id_token") String idToken,
        @JsonProperty("access_token") String accessToken,
        @JsonProperty("token_type") String tokenType,
        @JsonProperty("expires_in") Long expiresIn,
        @JsonProperty("refresh_token") String refreshToken) {
        this.idToken = idToken;
        this.accessToken = accessToken;
        this.tokenType = tokenType;
        this.expiresIn = expiresIn;
        this.refreshToken = refreshToken;
    }

    public String getIdToken() {
        return idToken;
    }

    public String getAccessToken() {
        return accessToken;
    }

    public String getTokenType() {
        return tokenType;
    }

    public Long getExpiresIn() {
        return expiresIn;
    }

    public String getRefreshToken() {
        return refreshToken;
    }

    @Override
    public String toString() {
        return String.format("idToken = %s,\n accessToken = %s,\n tokenType = %s,\n expiresIn = %d,\n refreshToken = %s,\n",
            idToken, accessToken, tokenType, expiresIn, refreshToken);
    }
}
