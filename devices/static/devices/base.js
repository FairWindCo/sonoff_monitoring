function set_per_page(number, url){
    url += "?per_page="+number;
    window.location.href = url;
}

function hide_offline_blocks(){
    const hide_offline_element = $('#hide_offline');
    const hide_offline = hide_offline_element?hide_offline_element.is(':checked'):false;
    if(hide_offline){
        $('[device-data-id] .alert-secondary').hide();
    } else {
        $('[device-data-id] .alert-secondary').show();
    }
}
var devices_temp = {};
var devices_hom = {};
function data_gaudge_refresh(timeout, url, params_data) {
    console.log(url);
    if(timeout <= 0 && data_gaudge_refresh.hasOwnProperty('data_gaudge_refresh')){
        clearTimeout(data_gaudge_refresh.refresh_timer);
    }

    delete data_gaudge_refresh.refresh_timer;

    $.ajax(url, {
        'data':params_data,
        'success':function (data, status) {
            if(Array.isArray(data)){
                const hide_offline_element = $('#hide_offline');
                const hide_offline = hide_offline_element?hide_offline_element.is(':checked'):false;
                for (index in data){
                    if(data[index].hasOwnProperty('id')){
                        let gaudge = devices_temp['DEV_'+data[index].id];
                        if(gaudge !== undefined){
                            gaudge.setValue(data[index]['temperature'])
                        }
                        gaudge = devices_hom['DEV_'+data[index].id];
                        if(gaudge !== undefined){
                            gaudge.setValue(data[index]['humidity'])
                        }
                        if(hide_offline && !data[index]['on_line']){
                            $('[device-data-id='+data[index].id+']').hide();
                        } else {
                            $('[device-data-id='+data[index].id+']').show();
                        }
                    }
                }
            } else {
                console.log('ERROR DATA:', data)
            }
            if(timeout>0) {
                data_gaudge_refresh.refresh_timer=setTimeout(data_gaudge_refresh, timeout, timeout, url, params_data);
            }
        }
    });
}

function data_refresh(timeout, url, params_data) {
    console.log(url);
    if(timeout <= 0 && data_refresh.hasOwnProperty('refresh_timer')){
        clearTimeout(data_refresh.refresh_timer);
    }

    delete data_refresh.refresh_timer;

    $.ajax(url, {
        'data':params_data,
        'success':function (data, status) {
            if(Array.isArray(data)){
                const hide_offline_element = $('#hide_offline');
                const hide_offline = hide_offline_element?hide_offline_element.is(':checked'):false;
                for (index in data){
                    if(data[index].hasOwnProperty('id')){
                        dev_row=$('[device-data-id='+data[index].id+']');
                        if(dev_row && dev_row.length == 1) {
                            if(!dev_row.hasClass('alert')) {
                                alert_element = dev_row.find('.alert');
                            } else {
                                alert_element = dev_row;
                            }
                            d_status = 0;
                            for(name in data[index]){
                                if(name == 'id' || !name) continue;
                                element = dev_row.find('[device-data-'+name+']');
                                if(element && element.length == 1) {
                                    value = data[index][name]
                                    if(value === undefined || value === null){
                                        value = '--';
                                    }

                                    if(name=='switch'){
                                        if(value){
                                            value = '<i class="fas fa-plug"></i>'
                                        } else {
                                            value = '<i class="far fa-times-circle"></i>'
                                        }
                                    }

                                    if(name == 'humidity'){
                                        value = value + ' % ';
                                        if(data[index].hasOwnProperty('status_hum')){
                                            if(data[index]['status_hum'] == 1){
                                                value = value + '<i class="far fa-bell"></i>';
                                                if(d_status<1){
                                                    d_status=1;
                                                }
                                            } else if(data[index]['status_hum'] == 2){
                                                value = value + '<i class="far fa-bell"></i>';
                                                if(d_status<1){
                                                    d_status=1;
                                                }
                                            } else if(data[index]['status_hum'] == 3){
                                                value = value + '<i class="fas fa-exclamation-triangle"></i>';
                                                if(d_status<2){
                                                    d_status=2;
                                                }
                                            } else if(data[index]['status_hum'] == 4){
                                                value = value + '<i class="fas fa-exclamation-triangle"></i>';
                                                if(d_status<2){
                                                    d_status=2;
                                                }
                                            }
                                        }
                                    } else if(name == 'temperature'){

                                        value = value + ' °C ';
                                        if(data[index].hasOwnProperty('status_temp')){
                                            if(data[index]['status_temp'] == 1){
                                                value = value + '<i class="far fa-bell"></i><i class="fas fa-temperature-low"></i>';
                                                if(d_status<1){
                                                    d_status=1;
                                                }
                                            } else if(data[index]['status_temp'] == 2){
                                                value = value + '<i class="far fa-bell"></i><i class="fas fa-temperature-high"></i>';
                                                if(d_status<1){
                                                    d_status=1;
                                                }
                                            } else if(data[index]['status_temp'] == 3){
                                                value = value + '<i class="fas fa-exclamation-triangle"></i><i class="fas fa-temperature-low"></i>';
                                                if(d_status<2){
                                                    d_status=2;
                                                }
                                            } else if(data[index]['status_temp'] == 4){
                                                value = value + '<i class="fas fa-exclamation-triangle"></i><i class="fas fa-temperature-high"></i>';
                                                if(d_status<2){
                                                    d_status=2;
                                                }
                                            }
                                        }
                                    }
                                    if(name=='on_line'){
                                        if(value){
                                            value = '<i class="fas fa-broadcast-tower"></i>';
                                        } else {
                                            value = '<i class="fas fa-times"></i>';
                                            d_status = 3;
                                        }
                                    }

                                    element.html(value);

                                } else {
                                    console.log(name, data[index][name]);
                                }
                            }

                        }
                        if(alert_element && alert_element.length>0){
                            alert_element.removeAttr('class');
                            alert_element.addClass('alert');
                            alert_element.show();
                            if(d_status==0){
                                alert_element.addClass('alert-success');
                            } else if (d_status == 1){
                                alert_element.addClass('alert-warning');
                            } else if (d_status == 2){
                                alert_element.addClass('alert-danger');
                            } else if (d_status == 3){
                                alert_element.addClass('alert-secondary');
                                if(hide_offline){
                                    alert_element.hide();
                                }
                            }
                        }
                    }
                }
            } else {
                console.log('ERROR DATA:', data)
            }
            if(timeout>0) {
                data_refresh.refresh_timer=setTimeout(data_refresh, timeout, timeout, url, params_data);
            }
        }
    });
}


function printit(){
                window.print() ;
}
function printit2(){
                window.print() ;
                window.close();
}
function moveBack(){
                if(window.history.length>1){
                    window.history.go(-1);
                } else {
                    window.close();
                }
                return false;
}
