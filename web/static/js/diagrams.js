jQuery(document).ready(function () {

    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/clouds");
    editor.session.setMode("ace/mode/python");

    $("#btn_1").click(function(){
      editor.setValue(example_1.trim());
      $("#diagrams_data").val(editor.getSession().getValue());
      $("#diagrams_form").submit();
    });
    $("#btn_2").click(function(){
      var text = example_2.trim()
      editor.setValue(text);
      $("#diagrams_data").val(editor.getSession().getValue());
      $("#diagrams_form").submit();
    });
    $("#btn_3").click(function(){
      var text = example_3.trim()
      editor.setValue(text);
      $("#diagrams_data").val(editor.getSession().getValue());
      $("#diagrams_form").submit();
    });
    $("#btn_more").click(function(){
      window.open("https://diagrams.mingrammer.com/docs/getting-started/examples", "_blank");
    });
    $("#build").click(function(){
      $("#diagrams_data").val(editor.getSession().getValue());
      $("#diagrams_form").submit();
    });

    $("#open_help").click(function(){
      document.getElementById("mySidenav").style.width = "30%";
      document.getElementById("main").style.marginLeft = "30%";
      $("#close_help").show();
      $("#open_help").hide();
    });

    $("#close_help").click(function(){
      document.getElementById("mySidenav").style.width = "0";
      document.getElementById("main").style.marginLeft = "0";
      $("#open_help").show();
      $("#close_help").hide();
    });
});

var example_1 =`
  from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

with Diagram("Grouped Workers", show=False, direction="TB"):
    ELB("lb") >> [EC2("worker1"),
                  EC2("worker2"),
                  EC2("worker3"),
                  EC2("worker4"),
                  EC2("worker5")] >> RDS("events")`

var example_2 =`
  from diagrams import Cluster, Diagram
from diagrams.gcp.analytics import BigQuery, Dataflow, PubSub
from diagrams.gcp.compute import AppEngine, Functions
from diagrams.gcp.database import BigTable
from diagrams.gcp.iot import IotCore
from diagrams.gcp.storage import GCS

with Diagram("Message Collecting", show=False):
    pubsub = PubSub("pubsub")

    with Cluster("Source of Data"):
        [IotCore("core1"),
         IotCore("core2"),
         IotCore("core3")] >> pubsub

    with Cluster("Targets"):
        with Cluster("Data Flow"):
            flow = Dataflow("data flow")

        with Cluster("Data Lake"):
            flow >> [BigQuery("bq"),
                     GCS("storage")]

        with Cluster("Event Driven"):
            with Cluster("Processing"):
                flow >> AppEngine("engine") >> BigTable("bigtable")

            with Cluster("Serverless"):
                flow >> Functions("func") >> AppEngine("appengine")

    pubsub >> flow`

var example_3 =`
  from diagrams import Cluster, Diagram
from diagrams.onprem.analytics import Spark
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka

with Diagram("Advanced Web Service with On-Premise", show=False):
    ingress = Nginx("ingress")

    metrics = Prometheus("metric")
    metrics << Grafana("monitoring")

    with Cluster("Service Cluster"):
        grpcsvc = [
            Server("grpc1"),
            Server("grpc2"),
            Server("grpc3")]

    with Cluster("Sessions HA"):
        master = Redis("session")
        master - Redis("replica") << metrics
        grpcsvc >> master

    with Cluster("Database HA"):
        master = PostgreSQL("users")
        master - PostgreSQL("slave") << metrics
        grpcsvc >> master

    aggregator = Fluentd("logging")
    aggregator >> Kafka("stream") >> Spark("analytics")

    ingress >> grpcsvc >> aggregator`
