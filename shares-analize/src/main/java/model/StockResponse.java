package model;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

@JsonInclude(JsonInclude.Include.NON_EMPTY)
public class StockResponse extends DBResponse {
    private final String company;
    private final String ticker;
    private final String sector;
    private final String industry;
    private final String country;
    private final String volume;
    private final String marketCapitalization;
    private final int employees;
    private final double price;
    private final double priceToEarnings;
    private final double priceToBook;
    private final double dividend;
    private final double debtToEquity;
    private List<ChartEntry> chart5Min;
    private List<ChartEntry> chart15Min;
    private String consistence;

    public StockResponse(String company, String ticker, String sector, String industry, String country, String volume,
        String marketCapitalization, int employees, double price, double priceToEarnings, double priceToBook, double dividend,
        double debtToEquity) {
        super("");
        this.company = company;
        this.ticker = ticker;
        this.sector = sector;
        this.industry = industry;
        this.country = country;
        this.volume = volume;
        this.marketCapitalization = marketCapitalization;
        this.employees = employees;
        this.price = price;
        this.priceToEarnings = priceToEarnings;
        this.priceToBook = priceToBook;
        this.dividend = dividend;
        this.debtToEquity = debtToEquity;
        this.chart5Min = new ArrayList<>();
        this.chart15Min = new ArrayList<>();
    }

    static public StockResponse create(ResultSet resultSet) throws SQLException {
        return new StockResponse(
            resultSet.getString("company"),
            resultSet.getString("ticker"),
            resultSet.getString("sector"),
            resultSet.getString("industry"),
            resultSet.getString("country"),
            resultSet.getString("volume"),
            resultSet.getString("market_capitalization"),
            resultSet.getInt("employees"),
            resultSet.getDouble("price"),
            resultSet.getDouble("priceToEarnings"),
            resultSet.getDouble("priceToBook"),
            resultSet.getDouble("dividend"),
            resultSet.getDouble("debtToEquity"));
    }

    public void set5MinChart(List<ChartEntry> chart) {
        this.chart5Min = chart;
    }

    public void set15MinChart(List<ChartEntry> chart) {
        this.chart15Min = chart;
    }

    public void setConsistence(String consistence) {
        this.consistence = consistence;
    }

    @JsonProperty("company")
    public String getCompany() {
        return company;
    }

    @JsonProperty("ticker")
    public String getTicker() {
        return ticker;
    }

    @JsonProperty("sector")
    public String getSector() {
        return sector;
    }

    @JsonProperty("industry")
    public String getIndustry() {
        return industry;
    }

    @JsonProperty("country")
    public String getCountry() {
        return country;
    }

    @JsonProperty("employees")
    public int getEmployees() {
        return employees;
    }

    @JsonProperty("price")
    public double getPrice() {
        return price;
    }

    @JsonProperty("pe_ratio")
    public double getPriceToEarnings() {
        return priceToEarnings;
    }

    @JsonProperty("price_to_book_ratio")
    public double getPriceToBook() {
        return priceToBook;
    }

    @JsonProperty("dividend")
    public double getDividend() {
        return dividend;
    }

    @JsonProperty("debt_to_equity")
    public double getDebtToEquity() {
        return debtToEquity;
    }

    @JsonProperty("volume")
    public String getVolume() {
        return volume;
    }

    @JsonProperty("market_capitalization")
    public String getMarketCapitalization() {
        return marketCapitalization;
    }

    @JsonProperty("chart_5min")
    public List<ChartEntry> getChart5Min() {
        return chart5Min;
    }

    @JsonProperty("chart_15min")
    public List<ChartEntry> getChart15Min() {
        return chart15Min;
    }

    @JsonProperty("consistence")
    public String getConsistence() {
        return consistence;
    }
}
