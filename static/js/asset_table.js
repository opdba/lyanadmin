/**
 * Created by melon on 2016/12/22.
 */

(function(jq){
    //点击checkbox样式变化
    function check_click_css() {
            $('.panel-body').delegate("tbody [type=checkbox]","click",function (event) {
            var isChecked=$(this).prop("checked");
            if (isChecked==false) {
            }else {
                $(this).parent().parent().addClass("checkbox_choice");
            }
            event.stopPropagation();    // event.stopPropagation();  //阻止checkbox的时间冒泡
        });
    }
    //end

    //选中一行 checkbox选中
    function tr_click_css() {
        $('.panel-body').delegate("tbody tr","click",function () {
            var isChecked=$(this).find("input:checkbox").prop("checked");
                if (isChecked==false) {
                    $(this).addClass("checkbox_choice");
                    $(this).find("input:checkbox").prop("checked", true);
                } else {
                    $(this).find("input:checkbox").prop("checked", false);
                    $(this).removeClass("checkbox_choice");
                }
        });
    }
    //end

    //阻止a标签的时间冒泡
    function stopPro_a() {
        $('.panel-body').delegate("tbody a","click",function(event){
         event.stopPropagation();   //阻止a标签的时间冒泡
     });
    }
    //end

    //表单提示框,确认后提交表单
    function boot_box_to(currentForm,message,t) {
        bootbox.dialog({
            message: message,
            title: "提示",
            // 退出dialog时的回调函数，包括用户使用ESC键及点击关闭
            onEscape: function() {
            },
            className: "my_modal_position",
            // dialog底端按钮配置
            buttons: {
                success: {
                    label: "确定",
                    className: "btn-success",
                    callback: function() {
                        $(currentForm).ajaxSubmit({
                             type: 'post', // 提交方式 get/post
                             success: function(data) { // data 保存提交后返回的数据，一般为 json 数据
                                // 此处可对 data 作相关处理
                                //  console.log(data);
                                 if (data == 'seccess'){
                                     $('#myModal').modal('hide');   //隐藏模态框
                                     $('#myModal_create').modal('hide');
                                     t.ajax.reload();   //刷新datatables
                                     setTimeout(function(){
                                         btn_box_alert("操作成功！");    //alert提示
                                        },500); //毫秒 防止右侧出现白条
                                 }
                                 else {
                                     setTimeout(function(){
                                         btn_box_alert("信息输入有误！: "+data);    //alert提示
                                        },500); //毫秒 防止右侧出现白条
                                 }
                            }
                        });
                      $(currentForm).resetForm(); // 提交后重置表单
                    }
                },
                Danger: {
                    label: "取消",
                    className: "btn-danger",
                    callback: function() {}
                }
            }
        });
    }
    //end

    //按钮提示框
    function btn_box_to(fun,message,url,t) {
        bootbox.dialog({
            message: message,
            title: "提示",
            // 退出dialog时的回调函数，包括用户使用ESC键及点击关闭
            onEscape: function() {},
            className: "my_modal_position",
            // dialog底端按钮配置
            buttons: {
                success: {
                  label: "确定",
                  className: "btn-success",
                  callback: function() {
                      // console.log(fun);
                      fun(url,t);
                }
            },
                Danger: {
                    label: "取消",
                    className: "btn-danger",
                    callback: function() {}
                }
            }
        });
    }
    //end

    //删除
    function del_choice(url,t) {
        var del_li = [];
        $('tbody :checked').each(function () {
            var del_id = $(this).parent().next().text();
            del_li.push(del_id);
            console.log(del_id);
        });
        console.log(del_li);
        var del_str = JSON.stringify(del_li);

        $.ajax({
            url: url,
            data: {obj : del_str},
            type: 'post',
            dataType: 'jsonp',//发送格式
            //callback和list相当于指定要发送的key和value，之后callback用来获取封装在list中的数据
            jsonp: 'callback',
            jsonpCallback: 'list',
            success: function(arg){
                // console.log(arg);   //arg,服务器返回的数据
                t.ajax.reload();
                setTimeout(function(){
                    btn_box_alert("删除成功！");    //alert提示
                                    },500); //毫秒 防止右侧出现白条
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){
                // console.log(XMLHttpRequest, textStatus, errorThrown);
                window.location.href="/asset/error/";
                // 当请求错误之后，自动调用
            }
        })
    }
    //end

    //alert提示框
    function btn_box_alert(message) {
        bootbox.dialog({
            message: message,
            size: 'small',
            // 退出dialog时的回调函数，包括用户使用ESC键及点击关闭
            onEscape: function() {},
            className: "my_modal_position",
            backdrop: false,
            // dialog底端按钮配置
            buttons: {
                alert: {
                    label: "确定"
                }
            }
        });
    }
    //end

    jq.extend({
        'da_table':function(content){
            var t = $(content).find("#asset_list").DataTable({
                destroy: true,
                paging: true,//分页
                pagingType: "full_numbers", //定义翻页组件的样式
                scrollX: "",    //宽度没有滚动条
                stateSave: false, //状态保存
                autoWidth: false, //自控制宽度
        // {#            serverSide: true,//分页，取数据等等的都放到服务端去#}
                processing: true, //载入数据的时候是否显示 载入中
                searching: true, //搜索
                pageLength: 10, //首次加载的数据条数

                ordering: false,    //排序操作在

                "aaSorting": [[4, 'desc']],

                ajax: {     //类似jquery的ajax参数，基本都可以用。
                    type: "post",   //后台指定了方式，默认get，外加datatable默认构造的参数很长，有可能超过get的最大长度。
                    url: "/asset/get_asset_list/",
                    dataSrc: "data",    //默认data，也可以写其他的，格式化table的时候取里面的数据
                },
                columns: [//对应上面thead里面的序列
                    { "data": null},
                    { "data": null},
                    { "data": "asset_id"},
                    { "data": "sn" },
                    { "data": "serial_name" },
                    { "data": "asset_type" },
                    { "data": "ip" },
                    { "data": "idc_name" },
                    { "data": "idc_jg" },
                    { "data": "projectname" },
                    { "data": "application" },
                    { "data": "module" },
                    { "data": "status" },
                    { "data": "linkman" },
                    { "data": "memo" },
                    { "data": "admin" },
                    { "data": "details" }
                ],

                "columnDefs": [
                    {
                        "targets": [ 3,9,12,14,15 ],
                        "visible": false    //隐藏列
                    },
                    {
                        targets: 2,
                        className: 'display_n'
                    },
                    {
                        targets: 1,
                        "render": function ( data, type, row, meta ) {
                            //<input type="checkbox">
                            return '<input type="checkbox" >';
                        }
                    },
                    {
                        targets: -1 ,//targets last column, use 0 for first column
                        className: 'pointer',
                        "data": "download_link",
                        "render": function ( data, type, row, meta ) {
                        //return '<a class="btn-link" href="'+row.id+'" target="_blank">'+ data +'</a>';
                         return '<a class="btn-link" href="'+row.asset_id+'">'+ data +'</a>';
                        }

                    },
                    {
                        "searchable": false,
                        "orderable": false,
                        "targets": 0
                    }
                ],
                "order": [[1, 'asc']],

                language: {
                     lengthMenu: '显示条数：<select class="form-control">' + '<option value="5">5</option>' + '<option value="10">10</option>' + '<option value="20">20</option>' + '<option value="30">30</option>' + '<option value="40">40</option>' + '<option value="50">50</option>' + '</select>',//左上角的分页大小显示。
                     search: '<span class="">搜索：</span>', //右上角的搜索文本，可以写html标签
                     processing: "载入中", //处理页面数据的时候的显示
                     paginate: { //分页的样式文本内容。
                         previous: "上一页",
                         next: "下一页",
                         first: "首页",
                         last: "尾页"
                    },
                    zeroRecords: "没有这条记录",//table tbody内容为空时，tbody的内容。
                    //下面三者构成了总体的左下角的内容。
                    info: "第_PAGE_/_PAGES_ 页，共 _TOTAL_ 条数据",//显示第_START_ 到第 _END_ 左下角的信息显示，大写的词为关键字。
                    infoEmpty: "0条记录",//筛选为空时左下角的显示。
                    infoFiltered: "筛选之后得到 _TOTAL_ 条，初始_MAX_ 条"//筛选之后的左下角筛选提示(另一个是分页信息显示，在上面的info中已经设置，所以可以不显示)，
                },

                "initComplete":function () {    //表格加载完成之后执行

                    $("tbody").find("a").click(function () {
                        event.stopPropagation();
                    });
                    //end
                }
            });
            // <!--添加索引-->
            t.on('order.dt search.dt',
                function() {
                    t.column(0, {
                    search: 'applied',
                    order: 'applied'
                    }).nodes().each(function(cell, i) {
                    cell.innerHTML = i + 1;
                    });
                }).draw();
            <!--end-->

            check_click_css();//点击checkbox样式变化
            tr_click_css();//选中一行 checkbox选中
            stopPro_a();//阻止a标签的时间冒泡


            <!--新建-->
            $("#asset_create").click(function () {
                btn_prem("/asset/btn_create/",cerate_model);
            });
            <!--end-->
            <!--编辑-->
            $("#asset_update").click(function () {
                btn_prem("/asset/btn_update/",update_model);
            });
            <!--end-->
            <!--编辑模态框-->
            function update_model() {
                var ck_number = $('tbody').find("input:checked");
                if (ck_number.length > 1){
                    btn_box_alert("最多只能选择一个进行修改！");
                }else if (ck_number.length == 0){
                    btn_box_alert("请选择要修改的数据！");
                    // $('#myModal_hint').modal({
                    //       keyboard: false
                    //     });
                }else {
                    var dt = $("#asset_list").dataTable();
                    var nTrs =dt.fnGetNodes();  //fnGetNodes获取表格所有行，nTrs[i]表示第i行tr对象
                    for(var i = 0; i < nTrs.length; i++){
                       if($(nTrs[i]).find("input:checkbox").prop("checked") == true){   //找出被选中的那行
                            var choice_data = dt.fnGetData(nTrs[i]);
                            // console.log(choice_data);//fnGetData获取一行的数据

                            var li=[];
                            $("#serial_name").val(choice_data.serial_name);
                            $("#ip").val(choice_data.ip);
                            $("#idc_jg").val(choice_data.idc_jg);
                            $("#module").val(choice_data.module);
                            $("#memo").val(choice_data.memo);

                           var pick_li = [choice_data.projectname,choice_data.application,choice_data.linkman,choice_data.asset_type,choice_data.idc_name,choice_data.status];
                           $('#myModal .selectpicker').find("option").each(function () {
                               var op_text = $(this).text();
                                for (var i = 0; i < pick_li.length; i++) {    //循环op_li列表
                                    if (pick_li[i] == op_text) {  //如果option的text在op_li列表内
                                        var val = $(this).val();    //取它的val
                                        $(this).parent().selectpicker('val',val); //设置初始值
                                    }
                                }
                           });
                       }
                    }

                    <!--激活模态框-->
                    $('#myModal').modal({
                          keyboard: false
                        });
                    <!--激活模态框-->
                }
            }
            //end
            // 新建模态框
            function cerate_model() {
                $('#myModal_create').modal({
                      keyboard: false
                    });
            }
            // end
            //按钮权限判断
            function btn_prem(url,fun) {
                $.ajax({
                    url: url,
                    data: {},
                    type: 'post',
                    dataType: 'jsonp',//发送格式
                    //callback和list相当于指定要发送的key和value，之后callback用来获取封装在list中的数据
                    jsonp: 'callback',
                    jsonpCallback: 'list',
                    success: function(arg){
                        // console.log(arg);   //arg,服务器返回的数据
                        fun()
                    },
                    error: function(XMLHttpRequest, textStatus, errorThrown){
                        // console.log(XMLHttpRequest, textStatus, errorThrown);
                        window.location.href="/asset/error/";
                        // 当请求错误之后，自动调用
                    }
                })
            }
            //end

            //删除二次确认
            $('#asset_delete').click(function () {
                var check_obj = $('tbody :checked');
                if (check_obj.length > 0){
                    var message="确定要删除选中数据吗?";
                    event.preventDefault();
                    btn_box_to(del_choice,message,'/asset/asset_delete/',t);  //传入执行函数,message,url,表格对象
                }else {
                    btn_box_alert("请选择要删除的数据！");
                }
            });
            //end

            //二次确认框
            // <!--编辑二次确认-->
            $("#amend_form").submit(function (event) {
                var currentForm = this;
                var message="确定要保存修改吗?";
                event.preventDefault();
                boot_box_to(currentForm,message,t);
            });

            // <!--新建二次确认-->
             $("#create_form").submit(function (event) {
                var currentForm = this;
                var message="确定要创建该数据吗?";
                event.preventDefault();
                boot_box_to(currentForm,message,t)

            });

            $("#dLabel").click(function () {
                $('#show_hide').toggle();
            });

            <!--隐藏/显示 列的点击事件-->
            $('.toggle-vis').on('click', function (e) {
                 e.preventDefault();
                 // console.log($(this).attr('data-column'));
                 var column = t.column($(this).attr('data-column'));
                 column.visible(!column.visible());
             });
            <!--end-->

            var show_check = $(".show_hide_check").find("li").each(function () {
                $(this).click(function () {
                    var show_isChecked=$(this).find("input:checkbox").prop("checked");
                    if (show_isChecked==false) {
                        // $(this).addClass("checkbox_choice");
                        $(this).find("input:checkbox").prop("checked", true);
                    } else {
                        $(this).find("input:checkbox").prop("checked", false);
                        // $(this).removeClass("checkbox_choice");
                    }
                });
            });

            //t为dataTables表格对象
            //colNum为操作列的序号 为整形数字
            function hidColumn(t, colNum) {
                var column = t.column(colNum);
                column.visible(!column.visible());
            }

            //checkbox的点击事件
            $(".show_hide_check").find("input:checkbox").click(function () {
                event.stopPropagation();  //阻止checkbox的时间冒泡

                var colNum = $(this).parent().attr('data-column');
                hidColumn(t,colNum)
            })

        },
        'log_table' :  function (content) {
            var t = $(content).find("#event_log_list").DataTable({
                destroy: true,
                paging: true,//分页
                pagingType: "full_numbers",//分页样式的类型
                stateSave: false, //状态保存
                autoWidth: false, //自控制宽度
                scrollX: "",    //宽度没有滚动条
                searching: true,//搜索
                pageLength: 10,//首次加载的数据条数
                ordering: false,//排序操作在服务端进行，所以可以关了。
                ajax: {//类似jquery的ajax参数，基本都可以用。
                    //type: "post",//后台指定了方式，默认get，外加datatable默认构造的参数很长，有可能超过get的最大长度。#}
                    url: "/asset/asset_event_logs/",
                    dataSrc: "data",//默认data，也可以写其他的，格式化table的时候取里面的数据
                    data: function (d) {//d 是原始的发送给服务器的数据，默认很长。
                    }
                },
                columns: [//对应上面thead里面的序列
                    {"data": null},
                    {"data": "event_type"},
                    {"data": "name"},
                    {"data": "component"},
                    {"data": "detail"},
                    {"data": "user"},
                    {"data": "date"}
                ],
                "columnDefs": [
                    {
                        "searchable": false,
                        "orderable": false,
                        "targets": 0
                    }
                ],
                "order": [[1, 'asc']],

                language: {
                    lengthMenu: '<select class="form-control input-xsmall">' + '<option value="5">5</option>' + '<option value="10">10</option>' + '<option value="20">20</option>' + '<option value="30">30</option>' + '<option value="40">40</option>' + '<option value="50">50</option>' + '</select>条记录',//左上角的分页大小显示。
                    search: '<span class="">搜索：</span>', //右上角的搜索文本，可以写html标签
                    processing: "载入中", //处理页面数据的时候的显示
                    paginate: { //分页的样式文本内容。
                        previous: "上一页",
                        next: "下一页",
                        first: "第一页",
                        last: "最后一页"
                    },
                    zeroRecords: "没有内容",//table tbody内容为空时，tbody的内容。
                    //下面三者构成了总体的左下角的内容。
                    info: "第_PAGE_/_PAGES_ 页，共 _TOTAL_ 条数据", //左下角的信息显示，大写的词为关键字。
                    infoEmpty: "0条记录",//筛选为空时左下角的显示。
                    infoFiltered: "筛选之后得到 _TOTAL_ 条，初始_MAX_ 条"
                }
            });
            // <!--添加索引-->
            t.on('order.dt search.dt',
                function () {
                    t.column(0, {
                        search: 'applied',
                        order: 'applied'
                    }).nodes().each(function (cell, i) {
                        cell.innerHTML = i + 1;
                    });
                }).draw();
            <!--end-->
        },
        'project_table' :  function (content) {
            var t = $(content).find("#project_list").DataTable({
                destroy: true,
                paging: true,//分页
                pagingType: "full_numbers",//分页样式的类型
                stateSave: false, //状态保存
                autoWidth: false, //自控制宽度
                scrollX: "",    //宽度没有滚动条
                searching: true,//搜索
                pageLength: 10,//首次加载的数据条数
                ordering: false,//排序操作在服务端进行，所以可以关了。
                ajax: {//类似jquery的ajax参数，基本都可以用。
                    type: "post",//后台指定了方式，默认get，外加datatable默认构造的参数很长，有可能超过get的最大长度。#}
                    url: "/asset/project_list/",
                    dataSrc: "data",//默认data，也可以写其他的，格式化table的时候取里面的数据
                    data: function (d) {//d 是原始的发送给服务器的数据，默认很长。
                    }
                },
                columns: [//对应上面thead里面的序列
                    {"data": null},
                    {"data": "choice"},
                    {"data": "project_id"},
                    {"data": "name"},
                    {"data": "memo"}
                ],
                "columnDefs": [
                    {
                        "searchable": false,
                        "orderable": false,
                        "targets": 0
                    },
                    {
                        targets: 1,
                        "render": function ( data, type, row, meta ) {
                            //<input type="checkbox">
                            return '<input type="checkbox" >';
                        }
                    },
                    {
                        targets: 2,
                        className: 'display_n'
                    },
                    {
                        targets: [ 0,1 ],
                        width : 20
                    }
                ],
                "order": [[1, 'asc']],

                language: {
                    lengthMenu: '<select class="form-control input-xsmall">' + '<option value="5">5</option>' + '<option value="10">10</option>' + '<option value="20">20</option>' + '<option value="30">30</option>' + '<option value="40">40</option>' + '<option value="50">50</option>' + '</select>条记录',//左上角的分页大小显示。
                    search: '<span class="">搜索：</span>', //右上角的搜索文本，可以写html标签
                    processing: "载入中", //处理页面数据的时候的显示
                    paginate: { //分页的样式文本内容。
                        previous: "上一页",
                        next: "下一页",
                        first: "第一页",
                        last: "最后一页"
                    },
                    zeroRecords: "没有内容",//table tbody内容为空时，tbody的内容。
                    //下面三者构成了总体的左下角的内容。
                    info: "第_PAGE_/_PAGES_ 页，共 _TOTAL_ 条数据", //左下角的信息显示，大写的词为关键字。
                    infoEmpty: "0条记录",//筛选为空时左下角的显示。
                    infoFiltered: "筛选之后得到 _TOTAL_ 条，初始_MAX_ 条"
                }
            });
            // <!--添加索引-->
            t.on('order.dt search.dt',
                function () {
                    t.column(0, {
                        search: 'applied',
                        order: 'applied'
                    }).nodes().each(function (cell, i) {
                        cell.innerHTML = i + 1;
                    });
                }).draw();
            <!--end-->
            check_click_css();//点击checkbox样式变化
            tr_click_css();//选中一行 checkbox选中
            stopPro_a();//阻止a标签的时间冒泡

            <!--新建-->
            $("#project_create").click(function () {
                btn_prem("/asset/btn_create/",cerate_model);
            });
            // 新建模态框
            function cerate_model() {
                $('#myModal_create').modal({
                      keyboard: false
                    });
            }
            // end

            <!--编辑-->
            $("#project_update").click(function () {
                btn_prem("/asset/btn_update/",update_model);

            });
            <!--end-->
            <!--编辑模态框-->
            function update_model() {
                var ck_number = $('tbody').find("input:checked");
                if (ck_number.length > 1){
                    btn_box_alert("最多只能选择一个进行修改！");
                }else if (ck_number.length == 0){
                    btn_box_alert("请选择要修改的数据！");
                    // $('#myModal_hint').modal({
                    //       keyboard: false
                    //     });
                }else {
                    var dt = $("#project_list").dataTable();
                    var nTrs =dt.fnGetNodes();  //fnGetNodes获取表格所有行，nTrs[i]表示第i行tr对象
                    for(var i = 0; i < nTrs.length; i++){
                       if($(nTrs[i]).find("input:checkbox").prop("checked") == true){   //找出被选中的那行
                            var choice_data = dt.fnGetData(nTrs[i]);
                            // console.log(choice_data);//fnGetData获取一行的数据
                            $("#id_update").val(choice_data.project_id);
                            $("#project_name_update").val(choice_data.name);
                            $("#memo_update").val(choice_data.memo);

                       }
                    }

                    <!--激活模态框-->
                    $('#myModal').modal({
                          keyboard: false
                        });
                    <!--激活模态框-->
                }
            }
            //end

            //按钮权限判断
            function btn_prem(url,fun) {
                $.ajax({
                    url: url,
                    data: {},
                    type: 'post',
                    dataType: 'jsonp',//发送格式
                    //callback和list相当于指定要发送的key和value，之后callback用来获取封装在list中的数据
                    jsonp: 'callback',
                    jsonpCallback: 'list',
                    success: function(arg){
                        // console.log(arg);   //arg,服务器返回的数据
                        fun()
                    },
                    error: function(XMLHttpRequest, textStatus, errorThrown){
                        // console.log(XMLHttpRequest, textStatus, errorThrown);
                        window.location.href="/asset/error/";
                        // 当请求错误之后，自动调用
                    }
                })
            }
            //end

            //二次确认框
            // 编辑二次确认
            $("#amend_form").submit(function (event) {
                var currentForm = this;
                var message="确定要保存修改吗?";
                event.preventDefault();
                boot_box_to(currentForm,message,t);
            });

            // 新建按钮二次确认
            $("#create_form").submit(function (event) {
                var currentForm = this;
                var message="确定要创建该数据吗?";
                event.preventDefault();
                boot_box_to(currentForm,message,t)

            });

            //删除二次确认
            $('#project_delete').click(function () {
                var check_obj = $('tbody :checked');
                if (check_obj.length > 0){
                    var message="确定要删除选中数据吗?";
                    event.preventDefault();
                    btn_box_to(del_choice,message,"/asset/project_delete/",t);  //传入执行函数和message
                }else {
                    btn_box_alert("请选择要删除的数据！");
                }
            });
            //end

        },
        'business_table' :  function (content) {
            var t = $(content).find("#business_list").DataTable({
                destroy: true, //加载时先删除原来table
                paging: true,//分页
                pagingType: "full_numbers",//分页样式的类型
                stateSave: false, //状态保存
                autoWidth: false, //自控制宽度
                scrollX: "",    //宽度没有滚动条
                searching: true,//搜索
                pageLength: 10,//首次加载的数据条数
                ordering: false,//排序操作在服务端进行，所以可以关了。
                ajax: {//类似jquery的ajax参数，基本都可以用。
                    type: "post",//后台指定了方式，默认get，外加datatable默认构造的参数很长，有可能超过get的最大长度。#}
                    url: "/asset/business_list/",
                    dataSrc: "data",//默认data，也可以写其他的，格式化table的时候取里面的数据
                    data: function (d) {//d 是原始的发送给服务器的数据，默认很长。
                    }
                },
                columns: [//对应上面thead里面的序列
                    {"data": null},
                    {"data": "choice"},
                    {"data": "business_id"},
                    {"data": "name"},
                    {"data": "memo"}
                ],
                "columnDefs": [
                    {
                        "searchable": false,
                        "orderable": false,
                        "targets": 0
                    },
                    {
                        targets: 1,
                        "render": function ( data, type, row, meta ) {
                            //<input type="checkbox">
                            return '<input type="checkbox" >';
                        }
                    },
                    {
                        targets: 2,
                        className: 'display_n'
                    },
                    {
                        targets: [ 0,1 ],
                        width : 20
                    }
                ],
                "order": [[1, 'asc']],

                language: {
                    lengthMenu: '<select class="form-control input-xsmall">' + '<option value="5">5</option>' + '<option value="10">10</option>' + '<option value="20">20</option>' + '<option value="30">30</option>' + '<option value="40">40</option>' + '<option value="50">50</option>' + '</select>条记录',//左上角的分页大小显示。
                    search: '<span class="">搜索：</span>', //右上角的搜索文本，可以写html标签
                    processing: "载入中", //处理页面数据的时候的显示
                    paginate: { //分页的样式文本内容。
                        previous: "上一页",
                        next: "下一页",
                        first: "第一页",
                        last: "最后一页"
                    },
                    zeroRecords: "没有内容",//table tbody内容为空时，tbody的内容。
                    //下面三者构成了总体的左下角的内容。
                    info: "第_PAGE_/_PAGES_ 页，共 _TOTAL_ 条数据", //左下角的信息显示，大写的词为关键字。
                    infoEmpty: "0条记录",//筛选为空时左下角的显示。
                    infoFiltered: "筛选之后得到 _TOTAL_ 条，初始_MAX_ 条"
                }
            });
            // <!--添加索引-->
            t.on('order.dt search.dt',
                function () {
                    t.column(0, {
                        search: 'applied',
                        order: 'applied'
                    }).nodes().each(function (cell, i) {
                        cell.innerHTML = i + 1;
                    });
                }).draw();
            <!--end-->
            check_click_css();//点击checkbox样式变化
            tr_click_css();//选中一行 checkbox选中
            stopPro_a();//阻止a标签的时间冒泡

            <!--新建-->
            $("#business_create").click(function () {
                btn_prem("/asset/btn_create/",cerate_model);
            });
            // 新建模态框
            function cerate_model() {
                $('#myModal_create').modal({
                      keyboard: false
                    });
            }
            // end

            <!--编辑-->
            $("#business_update").click(function () {
                btn_prem("/asset/btn_update/",update_model);

            });
            <!--end-->
            <!--编辑模态框-->
            function update_model() {
                var ck_number = $('tbody').find("input:checked");
                if (ck_number.length > 1){
                    btn_box_alert("最多只能选择一个进行修改！");
                }else if (ck_number.length == 0){
                    btn_box_alert("请选择要修改的数据！");
                    // $('#myModal_hint').modal({
                    //       keyboard: false
                    //     });
                }else {
                    var dt = $("#business_list").dataTable();
                    var nTrs =dt.fnGetNodes();  //fnGetNodes获取表格所有行，nTrs[i]表示第i行tr对象
                    for(var i = 0; i < nTrs.length; i++){
                       if($(nTrs[i]).find("input:checkbox").prop("checked") == true){   //找出被选中的那行
                            var choice_data = dt.fnGetData(nTrs[i]);
                            // console.log(choice_data);//fnGetData获取一行的数据
                            $("#id_update").val(choice_data.business_id);
                            $("#business_name_update").val(choice_data.name);
                            $("#memo_update").val(choice_data.memo);
                       }
                    }

                    <!--激活模态框-->
                    $('#myModal').modal({
                          keyboard: false
                        });
                    <!--激活模态框-->
                }
            }
            //end

            //按钮权限判断
            function btn_prem(url,fun) {
                $.ajax({
                    url: url,
                    data: {},
                    type: 'post',
                    dataType: 'jsonp',//发送格式
                    //callback和list相当于指定要发送的key和value，之后callback用来获取封装在list中的数据
                    jsonp: 'callback',
                    jsonpCallback: 'list',
                    success: function(arg){
                        // console.log(arg);   //arg,服务器返回的数据
                        fun()
                    },
                    error: function(XMLHttpRequest, textStatus, errorThrown){
                        // console.log(XMLHttpRequest, textStatus, errorThrown);
                        window.location.href="/asset/error/";
                        // 当请求错误之后，自动调用
                    }
                })
            }
            //end

            //二次确认框
            // 编辑二次确认
            $("#amend_form").submit(function (event) {
                var currentForm = this;
                var message="确定要保存修改吗?";
                event.preventDefault();
                boot_box_to(currentForm,message,t);
            });

            // 新建按钮二次确认
            $("#create_form").submit(function (event) {
                var currentForm = this;
                var message="确定要创建该数据吗?";
                event.preventDefault();
                boot_box_to(currentForm,message,t)

            });

            //删除二次确认
            $('#business_delete').click(function () {
                var check_obj = $('tbody :checked');
                if (check_obj.length > 0){
                    var message="确定要删除选中数据吗?";
                    event.preventDefault();
                    btn_box_to(del_choice,message,"/asset/business_delete/",t);  //传入执行函数和message
                }else {
                    btn_box_alert("请选择要删除的数据！");
                }
            });
            //end

        },
        'linkman_table' : function (content) {
            var t = $(content).find("#linkman_list").DataTable({
                paging: true,//分页
                pagingType: "full_numbers",//分页样式的类型
                scrollX: true,
                stateSave: true,
                searching: true,//搜索
                pageLength: 10,//首次加载的数据条数
                ordering: false,//排序操作在服务端进行，所以可以关了。
                ajax: {//类似jquery的ajax参数，基本都可以用。
                    type: "post",//后台指定了方式，默认get，外加datatable默认构造的参数很长，有可能超过get的最大长度。
                    url: "/asset/get_asset_linkman/",
                    dataSrc: "data",//默认data，也可以写其他的，格式化table的时候取里面的数据
                    data: function (d) {//d 是原始的发送给服务器的数据，默认很长。
    //                   return param;//自定义需要传递的参数。
                    }
                },
                columns: [//对应上面thead里面的序列
                    { "data": "id" },
                    { "data": "choice" },
                    { "data": "department" },
                    { "data": "name" },
                    { "data": "fixed_phone" },
                    { "data": "phone" },
                    { "data": "email" },
                    { "data": "qq" },
                    { "data": "memo" },
                ],

                "columnDefs": [
                    {
                        "targets":[1] ,
                        "render": function ( data, type, full, meta ) {
                            return "<input type='checkbox''/>";
                        }
                    }
                ],

                language: {
                     lengthMenu: '<select class="form-control input-xsmall">' + '<option value="5">5</option>' + '<option value="10">10</option>' + '<option value="20">20</option>' + '<option value="30">30</option>' + '<option value="40">40</option>' + '<option value="50">50</option>' + '</select>条记录',//左上角的分页大小显示。
                     search: '<span class="">搜索：</span>', //右上角的搜索文本，可以写html标签
                     processing: "载入中", //处理页面数据的时候的显示
                     paginate: { //分页的样式文本内容。
                         previous: "上一页",
                         next: "下一页",
                         first: "第一页",
                         last: "最后一页"
                    },
                    zeroRecords: "没有这条记录",//table tbody内容为空时，tbody的内容。
                    //下面三者构成了总体的左下角的内容。
                    info: "总共_PAGES_ 页，显示第_START_ 到第 _END_",//左下角的信息显示，大写的词为关键字。
                    infoEmpty: "0条记录",//筛选为空时左下角的显示。
                    infoFiltered: "筛选之后得到 _TOTAL_ 条，初始_MAX_ 条"//筛选之后的左下角筛选提示(另一个是分页信息显示，在上面的info中已经设置，所以可以不显示)，
                }
            })
        }
    });

})(jQuery);