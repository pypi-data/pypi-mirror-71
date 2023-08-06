{%- extends 'base.tpl' -%}
{% from 'mathjax.tpl' import mathjax %}

{# this overrides the default behavior of directly starting the kernel and executing the notebook #}
{% block notebook_execute %}
{% endblock notebook_execute %}

{% set nb_title = nb.metadata.get('title', '') or resources['metadata']['name'] %}

{%- block html_head_css -%}
<link href="{{resources.base_url}}voila/static/css/index.css" rel="stylesheet" type='text/css'>
{% if resources.theme == 'dark' %}
{% set bar_color = '#555454' %}
<link href="{{resources.base_url}}voila/static/css/theme-dark.css" rel="stylesheet" type='text/css'>
{% else %}
{% set bar_color = '#f3f700' %}
<link href="{{resources.base_url}}voila/static/css/theme-light.css" rel="stylesheet" type='text/css'>
{% endif %}
<link href="{{resources.base_url}}voila/static/css/mcloud_theme.min.css" rel="stylesheet" type='text/css'>

<style type="text/css">
body {
  background-color: var(--jp-layout-color0);
  overflow-y: scroll;
}

.nav-wrapper {
  background-color: {{ bar_color }};
}

/* Normal white Button as seen on Google.com*/
button {
  color: #444444;
  background: #F3F3F3;
  border: 1px #DADADA solid;
  padding: 5px 10px;
  border-radius: 2px;
  font-weight: bold;
  font-size: 9pt;
  outline: none;
}

button:hover {
  border: 1px #C6C6C6 solid;
  box-shadow: 1px 1px 1px #EAEAEA;
  color: #333333;
  background: #F7F7F7;
}

button:active {
  box-shadow: inset 1px 1px 1px #DFDFDF;
}

/* Blue button as seen on translate.google.com*/
button.blue {
  color: white;
  background: #4C8FFB;
  border: 1px #3079ED solid;
  box-shadow: inset 0 1px 0 #80B0FB;
}

button.blue:hover {
  border: 1px #2F5BB7 solid;
  box-shadow: 0 1px 1px #EAEAEA, inset 0 1px 0 #5A94F1;
  background: #3F83F1;
}

button.blue:active {
  box-shadow: inset 0 2px 5px #2370FE;
}

/* Orange button as seen on blogger.com*/
button.orange {
  color: white;
  border: 1px solid #FB8F3D;
  background: -webkit-linear-gradient(top, #FDA251, #FB8F3D);
  background: -moz-linear-gradient(top, #FDA251, #FB8F3D);
  background: -ms-linear-gradient(top, #FDA251, #FB8F3D);
}

button.orange:hover {
  border: 1px solid #EB5200;
  background: -webkit-linear-gradient(top, #FD924C, #F9760B);
  background: -moz-linear-gradient(top, #FD924C, #F9760B);
  background: -ms-linear-gradient(top, #FD924C, #F9760B);
  box-shadow: 0 1px #EFEFEF;
}

button.orange:active {
  box-shadow: inset 0 1px 1px rgba(0,0,0,0.3);
}

/* Red Google Button as seen on drive.google.com */
button.red {
  background: -webkit-linear-gradient(top, #DD4B39, #D14836);
  background: -moz-linear-gradient(top, #DD4B39, #D14836);
  background: -ms-linear-gradient(top, #DD4B39, #D14836);
  border: 1px solid #DD4B39;
  color: white;
  text-shadow: 0 1px 0 #C04131;
}

button.red:hover {
  background: -webkit-linear-gradient(top, #DD4B39, #C53727);
  background: -moz-linear-gradient(top, #DD4B39, #C53727);
  background: -ms-linear-gradient(top, #DD4B39, #C53727);
  border: 1px solid #AF301F;
}

button.red:active {
  box-shadow: inset 0 1px 1px rgba(0,0,0,0.2);
  background: -webkit-linear-gradient(top, #D74736, #AD2719);
  background: -moz-linear-gradient(top, #D74736, #AD2719);
  background: -ms-linear-gradient(top, #D74736, #AD2719);
}

.brand-logo {
  height: 90%;
  width: 100%;
}

#loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 75vh;
  color: var(--jp-content-font-color1);
  font-family: sans-serif;
}

.spinner {
  animation: rotation 2s infinite linear;
  transform-origin: 50% 50%;
}

.spinner-container {
  width: 10%;
}

@keyframes rotation {
  from {transform: rotate(0deg);}
  to   {transform: rotate(359deg);}
}

.voila-spinner-color1{
  fill: {{ bar_color }};
}

.voila-spinner-color2{
  fill: #f8e14b;
}

@font-face {
  font-family: 'Material Icons';
  font-style: normal;
  font-weight: 400;
  src: url({{resources.base_url}}voila/static/css/icons_font.ttf) format('truetype');
}

.material-icons {
  font-family: 'Material Icons';
  font-weight: normal;
  font-style: normal;
  font-size: 24px;
  line-height: 1;
  letter-spacing: normal;
  text-transform: none;
  display: inline-block;
  white-space: nowrap;
  word-wrap: normal;
  direction: ltr;
}
</style>

{% for css in resources.inlining.css %}
<style type="text/css">
{{ css }}
</style>
{% endfor %}

<style>
a.anchor-link {
  display: none;
}
.highlight  {
  margin: 0.4em;
}
</style>


{{ mathjax() }}
{%- endblock html_head_css -%}

{%- block body -%}
{%- block body_header -%}
<body data-base-url="{{resources.base_url}}voila/">
  <div id="loading">
    <div class="spinner-container">
      <svg class="spinner" data-name="c1" version="1.1" viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg" xmlns:cc="http://creativecommons.org/ns#" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><metadata><rdf:RDF><cc:Work rdf:about=""><dc:format>image/svg+xml</dc:format><dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage"/><dc:title>voila</dc:title></cc:Work></rdf:RDF></metadata><title>spin</title><path class="voila-spinner-color1" d="m250 405c-85.47 0-155-69.53-155-155s69.53-155 155-155 155 69.53 155 155-69.53 155-155 155zm0-275.5a120.5 120.5 0 1 0 120.5 120.5 120.6 120.6 0 0 0-120.5-120.5z"/><path class="voila-spinner-color2" d="m250 405c-85.47 0-155-69.53-155-155a17.26 17.26 0 1 1 34.51 0 120.6 120.6 0 0 0 120.5 120.5 17.26 17.26 0 1 1 0 34.51z"/></svg>
    </div>
    <h5 id="loading_text">Running {{nb_title}}...</h5>
  </div>
  <script>
  var voila_process = function(cell_index, cell_count) {
    var el = document.getElementById("loading_text")
    el.innerHTML = `Executing ${cell_index} of ${cell_count}`
  }
</script>

<div id="rendered_cells" style="display: none">
  {%- endblock body_header -%}

  <div class="mcloud-header header" id="mcloudHeader">
    <div class="navbar navbar-default navbar-static-top">
      <div class="container-fluid">
        <div class="navbar-header">
          <button class="navbar-toggle" data-target=".header-collapse"
          data-toggle="collapse" type="button">
          <span class="sr-only">Toggle navigation</span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </button>
        <a class="navbar-brand" href="https://www.materialscloud.org/home">
          <img src="{{ resources.base_url }}voila/static/images/mcloud_logo.png">
        </a>
      </div>

      <div class="collapse navbar-collapse header-collapse">
        <ul class="nav navbar-nav">
          <li><a href="https://www.materialscloud.org/learn">LEARN</a></li>
          <li class="active"><a ui-sref="main.work" href="https://www.materialscloud.org/work">WORK</a></li>
          <li><a href="https://www.materialscloud.org/discover">DISCOVER</a></li>
          <li><a href="https://www.materialscloud.org/explore">EXPLORE</a></li>
          <li><a href="https://www.materialscloud.org/archive">ARCHIVE</a></li>
        </ul>
      </div>
    </div>
  </div>
</div> <!-- End of header -->

<main style="padding: 5px; background-color: #f0f6f9" >
  <div class="container" style="margin: 40px auto">
    <div class="row">
      <div class="col s12" id="col_s12" style="margin-bottom: 30px">
        {% if resources.theme == 'dark' %}
        <div class="jp-Notebook theme-dark">
          {% else %}
          <div class="jp-Notebook theme-light">
            <ol class="breadcrumb ng-isolate-scope" ncy-breadcrumb="">
              <li ng-repeat="step in steps" ng-class="{active: $last}" ng-switch="$last || !!step.abstract" class="ng-scope" style="">
                <a ng-switch-when="false" href="https://www.materialscloud.org/work/" class="ng-binding ng-scope" style="">Work</a>
              </li>
              <li ng-repeat="step in steps" ng-class="{active: $last}" ng-switch="$last || !!step.abstract" class="ng-scope" style="">
                <a ng-switch-when="false" href="https://www.materialscloud.org/work/tools" class="ng-binding ng-scope" style="">Tools</a>
              </li>
              <li ng-repeat="step in steps" ng-class="{active: $last}" ng-switch="$last || !!step.abstract" class="ng-scope active" style="">
                <span ng-switch-when="true" class="ng-binding ng-scope">{{nb_title}}</span>
              </li>
            </ol>
            {% endif %}
            {%- block body_loop -%}
            {# from this point on, the kernel is started #}
            {%- with kernel_id = kernel_start() -%}
            <script id="jupyter-config-data" type="application/json">
            {
              "baseUrl": "{{resources.base_url}}",
              "kernelId": "{{kernel_id}}"
            }
            </script>
            {% set cell_count = nb.cells|length %}
            {%- for cell in cell_generator(nb, kernel_id) -%}
            {% set cellloop = loop %}
            {%- block any_cell scoped -%}
            <script>
            voila_process({{ cellloop.index }}, {{ cell_count }})
            </script>
            {{ super() }}
            {%- endblock any_cell -%}
            {%- endfor -%}
            {% endwith %}
            {%- endblock body_loop -%}
            <div id="rendered_cells" style="display: none">
            </div>
          </div>
        </div>
      </div>
    </main>

    {%- block body_footer -%}
    <script type="text/javascript">
    (function() {
      // remove the loading element
      var el = document.getElementById("loading")
      el.parentNode.removeChild(el)
      // show the cell output
      el = document.getElementById("rendered_cells")
      el.style.display = 'unset'
    })();
    </script>

    <script src="{{resources.base_url}}voila/static/js/materialize.min.js"></script>
  </body>
  {%- endblock body_footer -%}

  {% block footer_js %}
  {{ super() }}

  {% endblock footer_js %}

  {%- endblock body -%}
