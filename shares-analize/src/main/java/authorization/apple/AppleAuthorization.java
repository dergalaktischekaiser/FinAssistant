package authorization.apple;

import java.io.FileReader;
import java.io.IOException;
import java.security.PrivateKey;
import java.util.Date;

import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import io.jsonwebtoken.JwsHeader;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.io.Decoders;
import org.bouncycastle.asn1.pkcs.PrivateKeyInfo;
import org.bouncycastle.openssl.PEMParser;
import org.bouncycastle.openssl.jcajce.JcaPEMKeyConverter;

public class AppleAuthorization {

    private static String APPLE_AUTH_URL = "https://appleid.apple.com/auth/token";
    private static String KEY_ID = "KB6G7ACD96";
    private static String TEAM_ID = "RFR2B9U6J8";
    private static String CLIENT_ID = "com.tommystaroverov.mixApp";
    private static String PRIVATE_KEY_PATH = "/home/staroverovad/.cert/AuthKey_KB6G7ACD96.p8";

    private static ObjectMapper OBJECT_MAPPER = new ObjectMapper();

    private static PrivateKey pKey = null;

    private static PrivateKey getPrivateKey() throws IOException {
        //read your key
        final PEMParser pemParser = new PEMParser(new FileReader(PRIVATE_KEY_PATH));
        final JcaPEMKeyConverter converter = new JcaPEMKeyConverter();
        final PrivateKeyInfo object = (PrivateKeyInfo) pemParser.readObject();

        return converter.getPrivateKey(object);
    }

    private static String generateJWT() throws IOException {
        if (pKey == null) {
            pKey = getPrivateKey();
        }

        return Jwts.builder()
            .setHeaderParam(JwsHeader.KEY_ID, KEY_ID)
            .setIssuer(TEAM_ID)
            .setAudience("https://appleid.apple.com")
            .setSubject(CLIENT_ID)
            .setExpiration(new Date(System.currentTimeMillis() + (1000 * 60 * 5)))
            .setIssuedAt(new Date(System.currentTimeMillis()))
            .signWith(SignatureAlgorithm.ES256, pKey)
            .compact();
    }

    /*
     * Returns unique user id from apple
     * */
    public static String auth(String authorizationCode) throws IOException, UnirestException {
        OBJECT_MAPPER.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);

        String token = generateJWT();

        HttpResponse<String> response = Unirest.post(APPLE_AUTH_URL)
            .header("Content-Type", "application/x-www-form-urlencoded")
            .field("client_id", CLIENT_ID)
            .field("client_secret", token)
            .field("grant_type", "authorization_code")
            .field("code", authorizationCode)
            .asString();

        AppleTokenResponse appleTokenResponse = OBJECT_MAPPER.readValue(response.getBody(), AppleTokenResponse.class);
        System.err.println(appleTokenResponse);

        String payload = appleTokenResponse.getIdToken().split("\\.")[1];//0 is header we ignore it for now
        String decoded = new String(Decoders.BASE64.decode(payload));

        IdTokenPayload idTokenPayload = OBJECT_MAPPER.readValue(decoded, IdTokenPayload.class);
        return idTokenPayload.getSub();
    }
}