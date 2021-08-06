/*
 * Only useful in changelist pages when the ModelAdmin displayed has 
 * "list_editable" (https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_editable)
 * configured.
 *
 * When one of the input/select/textarea value is changed, automatically submit
 * the form using ajax.
 *
 * Only form fields relevant to the "list_editable" will trigger a form submit.
 *
 * This script uses the jQuery packaged with Django, and already made available
 * in the admin via django.jQuery.
 *
 * An easy way to add this script to the admin is to override the base_site.html
 * admin template (https://docs.djangoproject.com/en/dev/ref/contrib/admin/#overriding-vs-replacing-an-admin-template),
 * and add the following to it:
 *
 *    {% block footer %}{{ block.super }}
 *        <script type="text/javascript" src="{% static "js/admin_list_editable_autosubmit.js" %}"></script>
 *    {% endblock footer %}
 */
console.log(jQuery)
if (typeof django != 'undefined') {
    (function($) {
        "use strict";

        $(function() {
            console.log('hola')
            var form = $('#changelist-form');
            var inputs = $('#changelist-form input, #changelist-form select, #changelist-form textarea')  // all inputs
                .not('.action-select,#action-toggle,[name=action]')  // but not those specific to the admin
                .not('[type=hidden],[type=submit]');  // nor the hidden inputs or the submit button

            //$('#changelist-form [name=_save]').hide();

            function form_ajax_submit() {
                var data = form.serialize();
                data += '&_save=1';  // add the submit button
                console.log('ENTRO en el AJAX',form.attr('action'))
                $.post(form.attr('action'), data, display_message_from_answer);
            }

            function display_message_from_answer(answer) {
                $('.messagelist').remove();
                $('.breadcrumbs').after($(answer).find('.messagelist').fadeIn().delay(2000).fadeOut());
            };

            inputs.change(function() {
                console.log('CAMBIO');
                form_ajax_submit();
            });
        });
    })(jQuery);
}