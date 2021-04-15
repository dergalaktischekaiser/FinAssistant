package model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class ChangeFavouritesRequest {
    private final String company;

    public ChangeFavouritesRequest(
        @JsonProperty("company") String company) {
        this.company = company;
    }

    public String getCompany() {
        return company;
    }
}
