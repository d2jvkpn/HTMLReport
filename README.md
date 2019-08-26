A tool to generate data analysis html report with python3, with default image slides and table of contents implemented by javascript, and create html table tag by read local tsv file and variable fullfill. Third part packages required: pandas, BeautifulSoup4, jinja2, html5print.

Specify html data attributions:

1. data-file: remove a tag(class "check") if a file not exits, reset child(figure.myTable) with data, and reset image file(or files seperate by comma) of figure.mySlide.

2. data-file-match: remove a tag(class "check") if no match files, and reset image files of figure.mySlide.

3. data-file-notexist: remove a tag(class "check") if a file exits.

4. data-table-ncols: specify figure.myTable max columns of each table(split a pandas dataframe).

5. data-level: div children of id=main, an correspond level head(h1, h2, h3) will be create as first child.

6. reference process: id=reference (name="Reference").
