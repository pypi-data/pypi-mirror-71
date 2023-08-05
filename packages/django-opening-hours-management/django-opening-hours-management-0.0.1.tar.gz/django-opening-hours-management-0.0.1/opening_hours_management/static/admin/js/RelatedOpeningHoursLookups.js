(function($) {
    'use strict';

    function dismissAddOpeningHourPopup(win, newId, newRepr, objDisplay) {
        var id = win.name;
        var id_selector = interpolate('#%s', [id]);
        var id_display_selector = interpolate('#%s_display', [id]);
        $(id_display_selector).html(objDisplay);
        $(id_selector).val(newId);
        updateRelatedObjectLinks(id_selector);
        win.close();
    }

    function dismissChangeOpeningHourPopup(win, objId, newRepr, newId, objDisplay) {
        var id = win.name.replace(/^edit_/, '');
        var id_selector = interpolate('#%s', [id]);
        var id_display_selector = interpolate('#%s_display', [id]);
        $(id_display_selector).html(objDisplay);
        $(id_selector).val(newId);
        updateRelatedObjectLinks(id_selector);
        win.close();
    }

    function dismissDeleteOpeningHourPopup(win, objId) {
        var id = win.name.replace(/^delete_/, '');
        var id_selector = interpolate('#%s', [id]);
        var id_display_selector = interpolate('#%s_display', [id]);
        $(id_display_selector).html(gettext("No opening hours defined"));
        $(id_selector).val(null);
        updateRelatedObjectLinks(id_selector);
        win.close();
    }

    window.dismissAddOpeningHourPopup = dismissAddOpeningHourPopup;
    window.dismissChangeOpeningHourPopup = dismissChangeOpeningHourPopup;
    window.dismissDeleteOpeningHourPopup = dismissDeleteOpeningHourPopup;

})(django.jQuery);
