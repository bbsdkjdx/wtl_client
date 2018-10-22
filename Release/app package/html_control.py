src_table='''    <style type="text/css">
        .scrollTable {
            border: 1px solid #EB8;/*table没有外围的border，只有内部的td或th有border*/
        }
        .scrollTable table {
            border-collapse:collapse; /*统一设置两个table为细线表格*/
        }
        /*表头 div的第一个子元素**/
        .scrollTable table.thead{
            width:100%;
        }
        /*表头*/
        .scrollTable table.thead th{
            border: 1px solid #EB8;
            border-right:#C96;
            color:#fff;
            background: #FF8C00;/*亮桔黄色*/
        }
    
        /*能带滚动条的表身*/
        /*div的第二个子元素*/
        .scrollTable div{
            width:100%;
            height:200px;
            overflow:auto;/*必需*/
            scrollbar-face-color:#EB8;/*那三个小矩形的背景色*/
            scrollbar-base-color:#ece9d8;/*那三个小矩形的前景色*/
            scrollbar-arrow-color:#FF8C00;/*上下按钮里三角箭头的颜色*/
            scrollbar-track-color:#ece9d8;/*滚动条的那个活动块所在的矩形的背景色*/
            scrollbar-highlight-color:#800040;/*那三个小矩形左上padding的颜色*/
            scrollbar-shadow-color:#800040;/*那三个小矩形右下padding的颜色*/
            scrollbar-3dlight-color: #EB8;/*那三个小矩形左上border的颜色*/
            scrollbar-darkshadow-Color:#EB8;/*那三个小矩形右下border的颜色*/
        }
    
        /*能带滚动条的表身的正体*/
        .scrollTable table.tbody{
            width:100%;
            border: 1px solid #C96;
            border-right:#B74;
            color:#666666;
            background: #ECE9D8;
        }
    
        /*能带滚动条的表身的格子*/
        .scrollTable table.tbody td{
            border:1px solid #C96;
        }
    </style>
    <div class="scrollTable" style="width:100%;height: 100%;">
        <table class="thead">
            col_width_descriptors
            <tbody>
                <tr>
                    the_table_head_row
                </tr>
            </tbody>
        </table>

        <div style="height:100%;width:100%;">
            <table class="tbody" id="the_table_id" > 
                col_width_descriptors
                <tbody >
                   the_table_body
                </tbody>
            </table>
        </div>
    </div>'''

def create_table(_id,head_li,width_li,data_li,fun_clk_row):
    ret=src_table.replace('the_table_id',_id)
    s=r'<col width="%d"></col>'
    col_width_descriptors=''.join((s%(x) for x in width_li))+r'<col></col>'
    ret=ret.replace('col_width_descriptors',col_width_descriptors)
    ret=ret.replace('the_table_head_row',r'<th>'+r'</th><th>'.join([str(x) for x in head_li])+r'</th>')
    get_row=lambda li:r'<td>'+r'</td><td>'.join([str(x) for x in li])+r'</td>'
    s_tr='<tr onmousedown="%s(this)">'%(fun_clk_row)
    the_table_body=s_tr+(r'</tr>'+s_tr).join((get_row(x) for x in data_li))+r'</tr>'
    ret=ret.replace('the_table_body',the_table_body)
    import clipboard
    clipboard.s2cb(ret)
    return ret