package model;

import java.util.Set;

import com.fasterxml.jackson.annotation.JsonProperty;

public class FavouritesResponse extends DBResponse {
    private final Set<String> tickers;

    public FavouritesResponse(Set<String> tickers) {
        super("");
        this.tickers = tickers;
    }

    @JsonProperty("tickers")
    public Set<String> getTickers() {
        return tickers;
    }
}
