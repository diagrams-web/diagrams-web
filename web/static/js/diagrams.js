jQuery(document).ready(function () {

    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/clouds");
    editor.session.setMode("ace/mode/python");

    if (document.getElementById("sidenav").style.width == 0){
      $("#close_help").hide();
    }
    // Load examples data and submit
    $("#btn_1").click(function(){
      editor.setValue(example_1.trim());
      build_diagrams();
    });
    $("#btn_2").click(function(){
      var text = example_2.trim()
      editor.setValue(text);
      build_diagrams();
    });
    $("#btn_3").click(function(){
      var text = example_3.trim()
      editor.setValue(text);
      build_diagrams();
    });
    $("#btn_more").click(function(){
      window.open("https://diagrams.mingrammer.com/docs/getting-started/examples", "_blank");
    });

    $("#build").click(function(){
        build_diagrams();
    });

    function build_diagrams(){
        var diagrams_data = editor.getSession().getValue();
        $.ajax({
            data : {'diagrams_data': diagrams_data},
            type : 'POST',
            url : '/build'
        })
        .done(function(result) {
            if(result.pic_name){
              $("#render").html('<img src="static/diagrams/'+result.pic_name+'" alt="'+result.pic_name+'" />');
              $("#render").removeClass('error');
            }else if (result.error){
              $("#render").html('<h4>ERROR</h4><pre><code>'+result.error+'</code></pre>');
              $("#render").addClass('error');
            }
        });
    };

    // help side menu
    $("#open_help").click(function(){
      document.getElementById("sidenav").style.width = "30%";
      document.getElementById("main").style.marginLeft = "30%";
      $("#close_help").show();
      $("#open_help").hide();
    });

    $("#close_help").click(function(){
      document.getElementById("sidenav").style.width = "0";
      document.getElementById("main").style.marginLeft = "0";
      $("#open_help").show();
      $("#close_help").hide();
    });

    $(".one_provider").click(function(){
      $("#content_menu").empty();
      var data = $(this).data();
      $.ajax({
        type : 'GET',
        url : '/help/' + data.provider
      })
      .done(function(result) {
        $("#content_menu").html(result.content);
      });
    });

    $('body').on('click', 'a.import_class', function() {
      var data = $(this).data();
      var string_import = "from diagrams." + data.path + " import " + data.class;
      if (data.alias) {
        string_import = string_import + " as " + data.alias
      }
      var editor_content = string_import + "\n" + editor.getSession().getValue();
      editor.setValue(editor_content);
      editor.gotoLine(1, string_import.length, true);
    });

    $('.tooltip').mouseover(function(){
      $(this).children('span').show();
    }).mouseout(function(){
      $(this).children('span').hide();
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
from diagrams.aws.compute import ECS
from diagrams.aws.database import RDS, Aurora
from diagrams.aws.network import Route53, VPC

with Diagram("Simple Web Service with DB Cluster", show=False, filename="mysql"):
    dns = Route53("dns")
    web = ECS("service")

    with VPC('VPC'):
        # using cluster with an icon
        with Cluster("DB ClusterA", icon=ECS):
            db_master1 = RDS("main")
            db_master1 - [RDS("replica1"), RDS("replica2")]
        # using the node
        with Aurora("DB ClusterB") as db2:
            db_master2 = RDS("main")
            db_master2 - [RDS("replica1"), RDS("replica2")]

        dns >> web >> db_master1
        # link to/from cluster
        dns >> web >> db2`

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
        primary = Redis("session")
        primary - Redis("replica") << metrics
        grpcsvc >> primary

    with Cluster("Database HA"):
        primary = PostgreSQL("users")
        primary - PostgreSQL("replica") << metrics
        grpcsvc >> primary

    aggregator = Fluentd("logging")
    aggregator >> Kafka("stream") >> Spark("analytics")

    ingress >> grpcsvc >> aggregator`
