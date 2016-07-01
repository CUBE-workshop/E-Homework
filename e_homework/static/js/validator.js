/**
 * Created by longfangsong on 16/6/30.
 */
$(function () {
    $.ajaxSetup({
        async: false
    });
});
function Validator(csrf_token, object_to_validate, validated_called_func, url_to_send_value_to, other_object_to_send_with, user_validate_func) {
    this.object_wrapped = object_to_validate;
    this.url_to_send = url_to_send_value_to;
    this.data_objects = other_object_to_send_with;
    this.func = user_validate_func;
    this.validated = validated_called_func;
    this.validate = function () {
        if (this.object_wrapped.val() == "") {
            this.validated(false);
            return false;
        }
        var to_post = [
            {name: "csrfmiddlewaretoken", value: csrf_token},
            {name: this.object_wrapped.attr("name"), value: this.object_wrapped.val()}
        ];
        if (this.data_objects != null) {
            for (var i = 0; i < this.data_objects.length; ++i) {
                var data_obj = this.data_objects[i];
                to_post[to_post.length] = {name: data_obj.attr("name"), value: data_obj.val()};
            }
        }
        if (this.func != null && !this.func()) {
            if (this.validated != null) {
                this.validated(false);
            }
            return false;
        }
        var is_success = true;
        if (this.url_to_send != null) {
            $.post(this.url_to_send, to_post, function (ret) {
                is_success = ret.is_valid;
            });
        }
        if (this.validated != null) {
            this.validated(is_success);
        }
        return is_success;
    }
}
function ValidatorGroup(all_validators) {
    this.validators = all_validators;
    this.is_valid_last_time = [];
    for (var i = 0; i < this.validators.length; ++i) {
        this.is_valid_last_time[i] = false;
    }
    this.validate = function (which_to_validate) {
        if (which_to_validate == null) {
            for (var i = 0; i < this.validators.length; ++i) {
                this.is_valid_last_time[i] = this.validators[i].validate();
            }
        } else {
            this.is_valid_last_time[which_to_validate] = this.validators[which_to_validate].validate();
        }
    };
    this.isAllValid = function () {
        return this.is_valid_last_time.every(function (ele) {
            return ele;
        });
    }
}