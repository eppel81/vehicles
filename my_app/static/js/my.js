$(function () {

    // Связываем событие изменения select-выбора юзера с запросом ajax
    $('#selectUser').bind('change', getUserData);

    function getUserData() {
        //if ($('#selectUser').val() != '') {
            $.getJSON($SCRIPT_ROOT + '/get_userdata', {
                login: $('#selectUser').val(),
            }, function (data) {
                var select_item = $('#vehicles_user');

                // делаем всем елементам списка deselect
                $('#vehicles_user option:selected').each(function(){this.selected = false;});
                $('#vehicles_user').select2();
                select_item.empty();

                $('#user_id').val(data.id);
                //$('#login').val(data.login);
                //$('#password').val(data.password);
                $('#name').val(data.name);
                $('#admin').val(data.admin);

                if (data.locked) {
                    $('#locked').prop("checked", true);
                } else {
                    $('#locked').prop("checked", false);
                }

                // Список транспортов юзера
                $('#vehicles_user').attr('multiple', 'multiple');

                //console.log(data.all_vehicles.length);
                for (i = 0; i < data.all_vehicles.length; i++) {
                    if (isInArray(data.all_vehicles[i], data.user_vehicles))
                        $('<option selected>' + data.all_vehicles[i]['name'] + '</option>').appendTo(select_item);
                    else
                        $('<option>' + data.all_vehicles[i]['name'] + '</option>').appendTo(select_item);
                }
                $('#vehicles_user').select2();

            });
        //}
        return false;
    };

    //Проверим вхождение обекта в другой массив
    function isInArray(obj, objArr){
        var i=0;
        for (i=0; i<objArr.length; i++){
            if (obj['id'] == objArr[i]['id']) {
                return true;
            }
        }
        return false;
    }
});
