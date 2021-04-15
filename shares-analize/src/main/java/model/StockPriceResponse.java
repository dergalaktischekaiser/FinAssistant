package model;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class StockPriceResponse extends DBResponse {
    private final double price;
    private final double peRatio;
    private final double marketCapitalization;
    private final double ebitda;
    private final double eps;
    private final double dividend;
    private final double dividendPercentage;
    public StockPriceResponse(double price, double peRatio, double marketCapitalization, double ebitda, double eps,
        double dividend, double dividendPercentage) {
        super("");
        this.price = price;
        this.peRatio = peRatio;
        this.marketCapitalization = marketCapitalization;
        this.ebitda = ebitda;
        this.eps = eps;
        this.dividend = dividend;
        this.dividendPercentage = dividendPercentage;
    }

    @JsonProperty("price")
    public double getPrice() {
        return price;
    }

    @JsonProperty("pe_ratio")
    public double getPeRatio() {
        return peRatio;
    }

    @JsonProperty("market_capitalization")
    public double getMarketCapitalization() {
        return marketCapitalization;
    }

    @JsonProperty("ebitda")
    public double getEbitda() {
        return ebitda;
    }

    @JsonProperty("eps")
    public double getEps() {
        return eps;
    }

    @JsonProperty("dividend_value")
    public double getDividend() {
        return dividend;
    }

    @JsonProperty("devidend_percentage")
    public double getDividendPercentage() {
        return dividendPercentage;
    }
}
