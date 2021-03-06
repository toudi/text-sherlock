# -*- coding: utf-8 -*-
# refs: http://flask.pocoo.org/docs/quickstart/#redirects-and-errors

import os
from server import app
from flask import render_template, request, abort, Response
from core.sherlock import indexer, searcher, db
from core import settings as core_settings, FULL_INDEX_PATH
from core import SherlockMeta
from core.utils import debug, read_file, get_root_path_for_project
from template_filters import register_filters

# register template filters
register_filters(app)


def results_from_search_text(project, text, pagenum=1, isPath=False, type=None):
    """Returns the results from the search using the given text, populated with the transformed items
    """
    idx = indexer.Indexer().get_index(project).searcher()
    # find something in the index
    if isPath:
        results = idx.find_path(text)
    else:
        try:
            results = idx.find_text(text, pagenum, core_settings.RESULTS_PER_PAGE)
        except ValueError, e:
            # This assumes the value error resulted from an page count issue
            app.logger.error('Out of page bounds: %s' % e)
            return []
    # transform the results
    return results


def add_default_response(response):
    """Adds the default response parameters to the response.
    """
    response['site_banner_text'] = core_settings.SITE_BANNER_TEXT
    response['site_title'] = core_settings.SITE_TITLE
    response['site_banner_color'] = core_settings.SITE_BANNER_COLOR
    response['last_indexed'] = SherlockMeta.get('last_indexed') or 'Never'
    response['projects'] = core_settings.PROJECTS.keys()
    pass
    

@app.route('/')
def index():
    """Handles index requests
    """
    response = {
        "title" : u"Welcome",
        "projects": core_settings.PROJECTS.keys(),
    }
    add_default_response(response)
    return render_template('index.html', **response)


@app.route('/p/<project_name>')
def project(project_name):
    """Shows the search form, along with project browser
       so that the user could change the project
    """

    search_text = request.args.get('q')
    pagenum     = int(request.args.get('p', 1))

    response = {
        'selected_project': project_name,
        'form': search_text is None
    }

    if search_text:
        results = results_from_search_text(project_name, search_text, pagenum)
        response.update({
        'search_text': search_text,
            'results': results,
            'total_count': results.total_count,
            'page': {
                'current': pagenum,
                'previous': results.prev_pagenum,
                'next': results.next_pagenum,
                'count': len(results)
            }
        })

    add_default_response(response)

    return render_template('project.html', **response)


@app.route('/p/<project_name>/document', methods=['GET'])
def document(project_name):
    """Handles document display requests
    """
    http_status = 200
    root_dir = get_root_path_for_project(project_name)
    full_path = request.args.get('path')
    is_raw = (request.args.get('raw') == 'true')
    # allow `lines` or `hl` to highlight the target lines
    hl_str = request.args.get('lines') or request.args.get('hl', '')
    # if the full path wasn't appended, then append it (assumes path exist in default index path)
    if root_dir not in full_path:
        full_path = os.path.join(root_dir, full_path)

    search_text = request.args.get('q')
    pagenum = request.args.get('p')

    # perform the text search, get wrapped results
    results = results_from_search_text(project_name, full_path, isPath=True)
    if not results:
        app.logger.error('Unable to find document: %s' % full_path)
        abort(404)
    doc = results[0]

    # grab contents, if file gone, then send 404 error message
    try:
        doc_contents = read_file(full_path)
    except IOError:
        app.logger.error('Document no longer exists: %s' % full_path)
        doc_contents = "Document does not exist"
        http_status = 404

    if is_raw:
        # dump the document text
        return Response(doc_contents, mimetype='text/plain')
    db_record = db.get_raw_file_record(full_path)

    # build response
    response = {
        "title" : doc.filename,
        'html_css_class' : 'document',
        'doc' : doc,
        "doc_html": doc_contents,
        'line': int(request.args.get('line', 0))-1,
        'search_text' : search_text,
        'page_number' : pagenum,
        'last_modified' : db_record.get('mod_date'),
        'http_status' : http_status,
        'selected_project': project_name,
    }
    add_default_response(response)
    return render_template('document.html', **response), http_status