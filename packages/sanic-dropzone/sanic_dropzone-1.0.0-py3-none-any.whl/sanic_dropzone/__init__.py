# -*- coding: utf-8 -*-
"""
    flask_dropzone
    ~~~~~~~~~~~~~~

    :author: Grey Li <withlihui@gmail.com>
    :copyright: (c) 2017 by Grey Li.
    :license: MIT, see LICENSE for more details.
"""
import warnings
from sanic import Sanic 
from sanic.blueprints import Blueprint
from markupsafe import Markup
from .utils import random_filename, get_url  # noqa


#: defined normal file type
allowed_file_extensions = {
    'default': 'image/*, audio/*, video/*, text/*, application/*',
    'image': 'image/*',
    'audio': 'audio/*',
    'video': 'video/*',
    'text': 'text/*',
    'app': 'application/*'
}

class Dropzone:
    def __init__(self, app=None):
        self.app = app

        if app:
            self.init_app(app)

    def init_app(self, app):

        self.app = app

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['dropzone'] = Dropzone

        # settings
        app.config.setdefault('DROPZONE_SERVE_LOCAL', False)
        app.config.setdefault('DROPZONE_MAX_FILE_SIZE', 3)  # MB
        app.config.setdefault('DROPZONE_INPUT_NAME', 'file')
        app.config.setdefault('DROPZONE_ALLOWED_FILE_CUSTOM', False)
        app.config.setdefault('DROPZONE_ALLOWED_FILE_TYPE', 'default')
        app.config.setdefault('DROPZONE_MAX_FILES', 'null')
        # The timeout to cancel upload request in millisecond, default to 30000 (30 second).
        # Set a large number if you need to upload large file.
        # .. versionadded: 1.5.0
        app.config.setdefault('DROPZONE_TIMEOUT', None)  # millisecond, default to 30000 (30 second)

        # The view to redirect when upload was completed.
        # .. versionadded:: 1.4.1
        app.config.setdefault('DROPZONE_REDIRECT_VIEW', None)

        # Whether to send multiple files in one request.
        # In default, each file will send with a request.
        # Then you can use ``request.files.getlist('paramName')`` to
        # get a list of uploads.
        # .. versionadded:: 1.4.1
        app.config.setdefault('DROPZONE_UPLOAD_MULTIPLE', False)

        # When ``DROPZONE_UPLOAD_MULTIPLE`` set to True, this will
        # defined how many uploads will handled in per request.
        # .. versionadded:: 1.4.1
        app.config.setdefault('DROPZONE_PARALLEL_UPLOADS', 2)

        # When set to ``True``, it will add a csrf_token hidden field in upload form.
        # You have to install Flask-WTF to make it work properly, see details in docs.
        # .. versionadded:: 1.4.2

        # Add support to upload files when button was clicked.
        # .. versionadded:: 1.5.0
        app.config.setdefault('DROPZONE_UPLOAD_ACTION', '')
        app.config.setdefault('DROPZONE_UPLOAD_ON_CLICK', False)
        app.config.setdefault('DROPZONE_UPLOAD_BTN_ID', 'upload')

        # Add support to create dropzone inside ``<form>``.
        # .. versionadded:: 1.5.0
        app.config.setdefault('DROPZONE_IN_FORM', False)

        # messages
        app.config.setdefault('DROPZONE_DEFAULT_MESSAGE', "Drop files here or click to upload.")
        app.config.setdefault('DROPZONE_INVALID_FILE_TYPE', "You can't upload files of this type.")
        app.config.setdefault('DROPZONE_FILE_TOO_BIG',
                              "File is too big {{filesize}}. Max filesize: {{maxFilesize}}MiB.")
        app.config.setdefault('DROPZONE_SERVER_ERROR', "Server error: {{statusCode}}")
        app.config.setdefault('DROPZONE_BROWSER_UNSUPPORTED',
                              "Your browser does not support drag'n'drop file uploads.")
        app.config.setdefault('DROPZONE_MAX_FILE_EXCEED', "You can't upload any more files.")
        app.config.setdefault('DROPZONE_CANCEL_UPLOAD', "Cancel upload")
        app.config.setdefault('DROPZONE_REMOVE_FILE', "Remove file")
        app.config.setdefault('DROPZONE_CANCEL_CONFIRMATION', "You really want to delete this file?")
        app.config.setdefault('DROPZONE_UPLOAD_CANCELED', "Upload canceled")


    def create(self, action='', csrf=False, action_view='', **kwargs):

        if self.app.config['DROPZONE_IN_FORM']:
            return Markup('<div class="dropzone" id="myDropzone"></div>')

        if action:
            action_url = get_url(self.app, action, **kwargs)
        else:
            warnings.warn('The argument was renamed to "action" and will be removed in 2.0.')
            action_url = self.app.url_for(action_view, **kwargs)


        return Markup('''<form action="%s" method="post" class="dropzone" id="myDropzone"
        enctype="multipart/form-data"></form>''' % action_url)

    def load_css(self, css_url=None, version='5.2.0'):
        """Load Dropzone's css resources with given version.

        .. versionadded:: 1.4.4

        :param css_url: The CSS url for Dropzone.js.
        :param version: The version of Dropzone.js.
        """
        css_filename = 'dropzone.min.css'
        serve_local = self.app.config['DROPZONE_SERVE_LOCAL']

        if serve_local:
            css = '<link rel="stylesheet" href="%s" type="text/css">\n' % \
                  self.app.url_for('dropzone.static', filename=css_filename)
        else:
            css = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/dropzone@%s/dist/min/%s"' \
                  ' type="text/css">\n' % (version, css_filename)

        if css_url:
            css = '<link rel="stylesheet" href="%s" type="text/css">\n' % css_url
        return Markup(css)

    def load_js(self, js_url=None, version='5.2.0'):
        """Load Dropzone's js resources with given version.

        .. versionadded:: 1.4.4

        :param js_url: The JS url for Dropzone.js.
        :param version: The version of Dropzone.js.
        """
        js_filename = 'dropzone.min.js'
        serve_local = self.app.config['DROPZONE_SERVE_LOCAL']

        if serve_local:
            js = '<script src="%s"></script>\n' % self.app.url_for('dropzone.static', filename=js_filename)
        else:
            js = '<script src="https://cdn.jsdelivr.net/npm/dropzone@%s/dist/%s"></script>\n' % (version, js_filename)

        if js_url:
            js = '<script src="%s"></script>\n' % js_url
        return Markup(js)

    def style(self, css):
        """Add css to dropzone.
        :param css: style sheet code.
        """
        return Markup('<style>\n.dropzone{%s}\n</style>' % css)


    def config(self, redirect_url=None, custom_init='', custom_options='', **kwargs):
        """Initialize dropzone configuration.

        .. versionadded:: 1.4.4

        :param redirect_url: The URL to redirect when upload complete.
        :param custom_init: Custom javascript code in ``init: function() {}``.
        :param custom_options: Custom javascript code in ``Dropzone.options.myDropzone = {}``.
        :param **kwargs: Mirror configuration variable, lowercase and without prefix.
                         For example, ``DROPZONE_UPLOAD_MULTIPLE`` becomes ``upload_multiple`` here.
        """
        if custom_init and not custom_init.strip().endswith(';'):
            custom_init += ';'

        if custom_options and not custom_options.strip().endswith(','):
            custom_options += ','

        upload_multiple = kwargs.get('upload_multiple', self.app.config['DROPZONE_UPLOAD_MULTIPLE'])
        parallel_uploads = kwargs.get('parallel_uploads', self.app.config['DROPZONE_PARALLEL_UPLOADS'])

        if upload_multiple in [True, 'true', 'True', 1]:
            upload_multiple = 'true'
        else:
            upload_multiple = 'false'

        size = kwargs.get('max_file_size', self.app.config['DROPZONE_MAX_FILE_SIZE'])
        param = kwargs.get('input_name', self.app.config['DROPZONE_INPUT_NAME'])
        redirect_view = kwargs.get('redirect_view', self.app.config['DROPZONE_REDIRECT_VIEW'])

        if redirect_view is not None or redirect_url is not None:
            redirect_url = redirect_url or self.app.url_for(redirect_view)
            redirect_js = '''
            this.on("queuecomplete", function(file) {
            // Called when all files in the queue finish uploading.
            window.location = "%s";
            });''' % redirect_url
        else:
            redirect_js = ''

        max_files = kwargs.get('max_files', self.app.config['DROPZONE_MAX_FILES'])

        click_upload = kwargs.get('upload_on_click', self.app.config['DROPZONE_UPLOAD_ON_CLICK'])
        button_id = kwargs.get('upload_btn_id', self.app.config['DROPZONE_UPLOAD_BTN_ID'])
        in_form = kwargs.get('in_form', self.app.config['DROPZONE_IN_FORM'])
        cancelUpload = kwargs.get('cancel_upload', self.app.config['DROPZONE_CANCEL_UPLOAD'])
        removeFile = kwargs.get('remove_file', self.app.config['DROPZONE_REMOVE_FILE'])
        cancelConfirmation = kwargs.get('cancel_confirmation', self.app.config['DROPZONE_CANCEL_CONFIRMATION'])
        uploadCanceled = kwargs.get('upload_canceled', self.app.config['DROPZONE_UPLOAD_CANCELED'])

        if click_upload:
            if in_form:
                action = get_url(self.app, kwargs.get('upload_action', self.app.config['DROPZONE_UPLOAD_ACTION']))

                click_listener = '''
                dz = this; // Makes sure that 'this' is understood inside the functions below.

                document.getElementById("%s").addEventListener("click", function handler(e) {
                    e.currentTarget.removeEventListener(e.type, handler);
                    e.preventDefault();
                    e.stopPropagation();
                    dz.processQueue();
                });
                this.on("queuecomplete", function(file) {
                    // Called when all files in the queue finish uploading.
                    document.getElementById("%s").click();
                });
                ''' % (button_id, button_id)
                click_option = '''
                url: "%s",
                autoProcessQueue: false,
                // addRemoveLinks: true,
                ''' % action
            else:
                click_listener = '''
                dz = this;
                document.getElementById("%s").addEventListener("click", function handler(e) {dz.processQueue();});
                ''' % button_id

                click_option = '''
                autoProcessQueue: false,
                // addRemoveLinks: true,
                '''
            upload_multiple = 'true'
            parallel_uploads = max_files if isinstance(max_files, int) else parallel_uploads
        else:
            click_listener = ''
            click_option = ''

        allowed_file_type = kwargs.get('allowed_file_type', self.app.config['DROPZONE_ALLOWED_FILE_TYPE'])
        allowed_file_custom = kwargs.get('allowed_file_custom', self.app.config['DROPZONE_ALLOWED_FILE_CUSTOM'])

        if allowed_file_custom:
            allowed_type = allowed_file_type
        else:
            allowed_type = allowed_file_extensions[allowed_file_type]

        default_message = kwargs.get('default_message', self.app.config['DROPZONE_DEFAULT_MESSAGE'])
        invalid_file_type = kwargs.get('invalid_file_type', self.app.config['DROPZONE_INVALID_FILE_TYPE'])
        file_too_big = kwargs.get('file_too_big', self.app.config['DROPZONE_FILE_TOO_BIG'])
        server_error = kwargs.get('server_error', self.app.config['DROPZONE_SERVER_ERROR'])
        browser_unsupported = kwargs.get('browser_unsupported', self.app.config['DROPZONE_BROWSER_UNSUPPORTED'])
        max_files_exceeded = kwargs.get('max_file_exceeded', self.app.config['DROPZONE_MAX_FILE_EXCEED'])

        timeout = kwargs.get('timeout', self.app.config['DROPZONE_TIMEOUT'])
        if timeout:
            custom_options += 'timeout: %d,' % timeout

        return Markup('''<script>
        Dropzone.options.myDropzone = {
          init: function() {
              %s  // redirect after queue complete
              %s  // upload queue when button click
              %s  // custom init code
          },
          %s  // click upload options
          uploadMultiple: %s,
          parallelUploads: %d,
          paramName: "%s", // The name that will be used to transfer the file
          maxFilesize: %d, // MB
          acceptedFiles: "%s",
          maxFiles: %s,
          dictDefaultMessage: `%s`, // message display on drop area
          dictFallbackMessage: "%s",
          dictInvalidFileType: "%s",
          dictFileTooBig: "%s",
          dictResponseError: "%s",
          dictMaxFilesExceeded: "%s",
          dictCancelUpload: "%s",
          dictRemoveFile: "%s",
          dictCancelUploadConfirmation: "%s",
          dictUploadCanceled: "%s",
          %s  // custom options code
        };
        </script>
                ''' % (redirect_js, click_listener, custom_init, click_option,
                       upload_multiple, parallel_uploads, param, size, allowed_type, max_files,
                       default_message, browser_unsupported, invalid_file_type, file_too_big,
                       server_error, max_files_exceeded, cancelUpload, removeFile, cancelConfirmation,
                       uploadCanceled, custom_options))
