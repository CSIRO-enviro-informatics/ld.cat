from flask import Blueprint, render_template, redirect, request
import ldcat.config as config
import markdown
from flask import Markup
from ldcat.view.register import LociRegisterRenderer
from ldcat.model.dataset_renderer import DatasetRenderer
from ldcat.model.linkset_renderer import LinksetRenderer
from ldcat.model.def_renderer import DefRenderer
import harvester

routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
    return render_template(
        'index.html',
        title='loci.cat'
    )


@routes.route('/dataset/')
def datasets():
    uri = request.values.get('uri')
    if uri:
        # Load the single instance
        return DatasetRenderer(uri, request).render()

    # Load the register
    renderer = LociRegisterRenderer(
        request,
        '',
        "Dataset Register",
        "Register of all VoID Datasets",
        LociRegisterRenderer.DATASET_REGISTER,
        [config.URI_DATASET_CLASS],
        0,
        super_register=config.URI_BASE)

    return renderer.render()



@routes.route('/linkset/')
def linksets():
    uri = request.values.get('uri')
    if uri:
        # Load the single instance
        return LinksetRenderer(uri, request).render()

    # Load the register
    renderer = LociRegisterRenderer(
        request,
        '',
        "Linksets Register",
        "Register of all VoID Linksets",
        LociRegisterRenderer.LINKSET_REGISTER,
        [config.URI_LINKSET_CLASS],
        0,
        super_register=config.URI_BASE)

    return renderer.render()


@routes.route('/def/')
def defs():
    uri = request.values.get('uri')
    if uri:
        # Load the single instance
        return DefRenderer(uri, request).render()

    # Load the register
    renderer = LociRegisterRenderer(
        request,
        '',
        "Definitional Resources Register",
        "Register of all Definitional Resources",
        LociRegisterRenderer.DEFS_REGISTER,
        [config.URI_DEF_CLASS],
        0,
        super_register=config.URI_BASE)

    return renderer.render()


@routes.route('/tool/')
def tools():
    renderer = LociRegisterRenderer(
        request,
        'http://loci.cat/tool/',
        "Tools Register",
        "Register of all Tools",
        LociRegisterRenderer.TOOLS_REGISTER,
        [config.URI_TOOL_CLASS],
        0,
        super_register=config.URI_BASE)

    return renderer.render()


@routes.route('/about')
def about():
    import os

    # using basic Markdown method from http://flask.pocoo.org/snippets/19/
    with open(os.path.join(os.path.dirname(config.APP_DIR), 'README.md')) as f:
        content = f.read()

    # make images come from web dir
    # content = content.replace('view/static/system.svg',
    #                           '/static/system.svg')
    content = Markup(markdown.markdown(content))

    return render_template(
        'about.html',
        title='About',
        navs={},
        content=content
    )


@routes.route('/LICENSE')
def license():
    redirect('https://github.com/CSIRO-enviro-informatics/loci.cat/blob/master/LICENSE')
