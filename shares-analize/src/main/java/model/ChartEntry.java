package model;

import java.sql.Timestamp;

import com.fasterxml.jackson.annotation.JsonProperty;

public class ChartEntry {
    private final double open;
    private final double close;
    private final double low;
    private final double high;
    private final Timestamp timestamp;

    public ChartEntry(double open, double close, double low, double high, Timestamp timestamp) {
        this.open = open;
        this.close = close;
        this.low = low;
        this.high = high;
        this.timestamp = timestamp;
    }

    @JsonProperty("open")
    public double getOpen() {
        return open;
    }

    @JsonProperty("close")
    public double getClose() {
        return close;
    }

    @JsonProperty("low")
    public double getLow() {
        return low;
    }

    @JsonProperty("high")
    public double getHigh() {
        return high;
    }

    @JsonProperty("timestamp")
    public Timestamp getTimestamp() {
        return timestamp;
    }
}
