function fun(){
        $("#result").empty();
        key = $("#keyword").val()
        alert(key)
     $.getJSON({
        url: "http://47.242.133.237:5000/search/" + key,
        success: function (result) {
            // 获取返回的数据中我们需要的部分
		alert(result['result'])
            res = result.response.docs;
            
            // 利用for插入每一个结果
            if (res.length) {
                for (i = 0; i < res.length; i++) {
                    // 将返回的结果包装成HTML
                    resultItem =
                        `
                        <div class='col-md-12 mb-4'>
                            <div class='card mb-12 shadow-sm'>
                                <div class='card-body'>
                                    <h5>` +
                        res[i].name +
                        ` <small style='margin-left: 10px'>` +
                        res[i].author +
                        `</small> <small style='margin-left: 10px'>` +
                        res[i].year +
                        `</small></h5>
                                    <p class='text-muted' style='margin-bottom: 0.5em'>` +
                        res[i].unit +
                        `</p>
                                    <p class='card-text'>` +
                        res[i].abstract +
                        `</p>
                                </div>
                            </div>
                        </div>
                    `;
                    // 插入HTML到result中
                    $("#result").append(resultItem);
                }

            }
        }
    });
    }


// 在按下enter键的时候就搜索
$(document).keyup(function (event) {
    if (event.keyCode == 13) {
        alert("sss");
    }
});