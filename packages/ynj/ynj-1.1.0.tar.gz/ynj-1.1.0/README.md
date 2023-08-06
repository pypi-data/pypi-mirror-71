# ynj

Compile [Jinja](http://jinja.pocoo.org/) templates using [YAML](https://yaml.org/) variables!


## Installation
```
pip install ynj
```

## Usage

To use `ynj` you need yaml file with the variables, and a jinja template.
An example `values.yml` file:
```
  ---
  name: John
  surname: Collins
  jobs:
    - name: "Python developer"
      technologies: [Pyton, SQL]
    - name: "Database administrator"
      technologies: [PostgreSQL, Oracle]
```
A sample template:
```
  <h1>{{ name }} {{ surname }}</h2>
  <dl>
{% for job in jobs %}
      <dt>{{ job.name }}</dt>
      <dd>{{ ', '.join(job.technologies) }}</dd>
{% endfor %}
  </dl>
```
To fill the values into the template, run:
```
ynj < jobs.j2
```
You can override values also from command line:
```
ynj -t jobs.j2 -s "{name: Matt}"
```
More info: `ynj -h`.
