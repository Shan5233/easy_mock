//JavaScript代码区域
layui.use('table', function () {
    var table = layui.table //表格
    var $ = layui.$;
    //执行一个 table 实例
    table.render({
        elem: '#mock'
        , height: 550
        , defaultToolbar: ['filter', "exports", {  //自定义头部工具栏右侧图标。如无需自定义，去除该参数即可
            title: '提示'
            , layEvent: 'info'
            , icon: 'layui-icon-tips'
        }]
        , url: '/code/mock/test/' //数据接口
        , page: true //开启分页
        , toolbar: '#toolbarDemo' //开启工具栏，指向自定义工具栏模板选择器，详见文档
        , cols: [[ //表头
            {field: 'id', title: 'ID', width: 55}
            , {field: 'title', title: '接口名称', width: 200}
            , {field: 'methods', title: '请求方式', width: 90}
            , {field: 'url', title: 'url', width: 250}
            , {field: 'description', title: '接口描述', width: 270}
            , {field: 'resparams', title: '期待返回', width: 350}
            , {field: 'update_time', title: '更新时间', width: 160}
            , {fixed: 'right', align: 'center', toolbar: '#operation'}
        ]]
        , done: function (res, curr, count) {
            //如果是异步请求数据方式，res即为你接口返回的信息。
            //如果是直接赋值的方式，res即为：{data: [], count: 99} data为当前页数据、count为数据总长度
            console.log(res);
            //得到当前页码
            console.log(curr);
            //得到数据总量
            console.log(count);
        }

    });

    //监听行单击事件（单击事件为：rowDouble）
    table.on('row(listen)', function (obj) {
        var data = obj.data;  //显示当前行数据
        layer.alert(JSON.stringify(data), {
            title: '当前行数据：'
        });
    });

    //监听行工具栏事件
    table.on('tool(listen)', function (obj) { //注：tool 是工具条事件名，test 是 table 原始容器的属性 lay-filter="对应的值"
        var data = obj.data; //获得当前行数据
        var layEvent = obj.event; //获得 lay-event 对应的值（也可以是表头的 event 参数对应的值）
        var tr = obj.tr; //获得当前行 tr 的 DOM 对象（如果有的话）

        if (layEvent === 'del') { //删除
            layer.confirm('确认删除该条数据吗', function (index) {
                //向服务端发送删除指令
                var id = JSON.stringify(data.id)
                $.ajax({
                    type: "GET",
                    url: "/del",
                    data: {"id": id},  //将id传向后端，进行软删除
                    dataType: "json",
                    success: function (result) {
                        if (result['status'] == "0") {   //从前台取回的状态值
                            layer.close(index);
                            $(".layui-laypage-btn").click();
                            //同步更新表格和缓存对应的值
                            obj.del();
                            layer.msg("删除成功");
                        } else {
                            layer.msg("删除失败");
                        }
                    },
                    error: function () {
                        layer.msg("删除失败");
                        layer.close(index);
                    }
                })
            });
        } else if (layEvent === 'edit') { //编辑
            //do something
        }
    });

    //监听头工具栏事件
    table.on('toolbar(listen)', function (obj) {
        var checkStatus = table.checkStatus(obj.config.id);
        switch (obj.event) {
            case 'add':
                //layer.msg('添加mock接口');
                layer.open({
                    type: 1,
                    title: '添加需要mock的接口',
                    area: ['60%', '80%'],
                    content: $("#tanchu"),
                    btn: ['提交', '取消'],
                    scrollbar: true //屏蔽浏览器滚动条
                    , success: function (layero, index) {

                    }, yes: function (index, layero) {
                        layero.find('form').find('button[lay-submit]').click(); //此处代码即为触发表单提交按钮


                    }, cancel: function (index, layero) {
                        //弹出层右上角关闭按钮的回调
                        layer.close(index);
                        location.reload();
                        //return false 开启该代码可禁止点击该按钮关闭
                    }, btn2: function (index, layero) {
                        //取消按钮的回调
                        layer.close(index);
                        location.reload();
                    },
                });
                //监听表单提交
                form.on('submit(go)', function (data) {
                    $.ajax({
                        type: "POST",
                        url: "/add",
                        data: data.field,
                        dataType: "json",
                        success: function (result) {
                            if (result['status'] == "0") {   //从前台取回的状态值
                                layer.close(index);
                                //同步更新表格和缓存对应的值
                                return false;
                                layer.msg("添加成功");
                                $(".layui-laypage-btn").click();
                            } else {
                                layer.msg("添加失败");
                            }
                        },
                        error: function () {
                            layer.msg("添加失败");
                        }
                    })
                });
                break;
            case 'info':
                layer.alert('功能还不够完善，请多多谅解~');
                break;
        }
    });

    //分页
    laypage.render({
        elem: 'pageDemo' //分页容器的id
        , count: 100 //总页数
        , skin: '#1E9FFF' //自定义选中色值
        //,skip: true //开启跳页
        , jump: function (obj, first) {
            if (!first) {
                layer.msg('第' + obj.curr + '页', {offset: 'b'});
            }
        }
    });

});

