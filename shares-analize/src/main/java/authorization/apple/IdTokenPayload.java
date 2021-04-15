package authorization.apple;

import com.fasterxml.jackson.annotation.JsonProperty;

public final class IdTokenPayload {
    private final String iss;
    private final String aud;
    private final Long exp;
    private final Long iat;
    private final String sub;//users unique id
    private final String atHash;
    private final Long authTime;
    private final Boolean nonceSupported;

    public IdTokenPayload(@JsonProperty("iss") String iss,
        @JsonProperty("aud") String aud,
        @JsonProperty("exp") Long exp,
        @JsonProperty("iat") Long iat,
        @JsonProperty("sub") String sub,
        @JsonProperty("at_hash") String atHash,
        @JsonProperty("auth_time") Long authTime,
        @JsonProperty("nonce_supported") Boolean nonceSupported) {
        this.iss = iss;
        this.aud = aud;
        this.exp = exp;
        this.iat = iat;
        this.sub = sub;
        this.atHash = atHash;
        this.authTime = authTime;
        this.nonceSupported = nonceSupported;
    }

    public String getSub() {
        return sub;
    }

    public String getIss() {
        return iss;
    }

    public String getAud() {
        return aud;
    }

    public Long getExp() {
        return exp;
    }

    public Long getIat() {
        return iat;
    }

    public String getAtHash() {
        return atHash;
    }

    public Long getAuthTime() {
        return authTime;
    }


    @Override
    public String toString() {
        return String.format("sub = %s,\n iss = %s,\n aud = %s,\n exp = %d,\n iat = %d,\n atHash = %s,\n authTime = %d",
            sub, iss, aud, exp, iat, atHash, authTime);
    }
}