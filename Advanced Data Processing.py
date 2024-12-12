import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
import org.apache.flink.api.common.serialization.SimpleStringSchema;

public class WasteStreamProcessor {
    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        Properties properties = new Properties();
        properties.setProperty("bootstrap.servers", "localhost:9092");
        properties.setProperty("group.id", "waste-group");

        DataStream<String> stream = env.addSource(new FlinkKafkaConsumer<>("waste_data", new SimpleStringSchema(), properties));

        // Complex event processing
        stream
            .keyBy(data -> JSON.parseObject(data).getString("bin_id"))
            .flatMap(new WasteAnomalyDetector())
            .addSink(new AlertSink());

        env.execute("Waste Management Stream Processing");
    }
}
