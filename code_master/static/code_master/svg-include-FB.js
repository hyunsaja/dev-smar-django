//임시 저장 관련 전역변수 사용경우 확인

var svgNS = "http://www.w3.org/2000/svg";
var svg = null;
var svg_standard = null;
var svg_submaterial = null;
var svg_macro = null;
var svgWidth = 0;  // 자재길이

var svgHeight = 0;
var svgThickness = 0;


var svg_data_ID = 1;
var svg_attr = "";
var svgSelectObject = null;

//=========================================


//사용지하 않음
function getRandomNumber(min, max) {
    var ranNum = Math.floor(Math.random() * (max - min + 1)) + min;
    return ranNum;
}
function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

//event
function makeID8Event(domObj, macro, A, dist) {
    var newDomObj = domObj;
    svg_data_ID++;
    newDomObj.setAttribute("id", "svg_id_" + svg_data_ID);
    newDomObj.setAttribute("name", "svg_name_" + svg_data_ID);

    newDomObj.setAttribute("data-id", "" + (svg_data_ID)); //사용하지 않으나 필요할수도
    newDomObj.setAttribute("data-dist", "" + dist);
    newDomObj.setAttribute("data-macro", "" + macro);
    newDomObj.setAttribute("data-a", "" + A);

    newDomObj.setAttribute("onmouseover", "svgEventOnMouseOver(this);");
    newDomObj.setAttribute("onmouseout", "svgEventOnMouseOut(this);");
    newDomObj.setAttribute("onclick", "svgEventOnClick(this);");

    return newDomObj;
}
function svgEventOnMouseOver(obj) {
    console.log(obj.id + " svgEventOnMouseOver");
    svg_attr = obj.getAttribute("style");
    obj.setAttribute("style", "fill:none; stroke:#ff0000; stroke-width:4;");
}
function svgEventOnMouseOut(obj) {
    if (svgSelectObject == null)
        obj.setAttribute("style", svg_attr);
}
function svgEventOnClick(obj) {
    if (obj == null) return;
    svgSelectObject = obj;
    console.log(obj.id + " svgEventOnClick");

    //Edit mode
    setEditMode();

    //색반영
    console.log(obj.id + " svgEventOnMouseOver");
    obj.setAttribute("style", "fill:none; stroke:" + getRandomColor() + "; stroke-width:4;");

    //데이터 폼에 반영
    var svg_data_id = document.getElementById("svg_data_id");
    var svg_dist = document.getElementById("svg_dist");
    var svg_macro = document.getElementById("svg_macro");
    var svg_A = document.getElementById("svg_A");

    svg_data_id.value = obj.getAttribute("data-ID");
    svg_dist.value = obj.getAttribute("data-dist");
    svg_macro.value = obj.getAttribute("data-macro");
    svg_A.value = obj.getAttribute("data-A");

}

//function
function setEditMode() {
    //수정 삭제버튼 확성화
    var svg_myDrawElement = document.getElementById("svg_myDrawElement");
    var svg_myEditElement = document.getElementById("svg_myEditElement");
    var svg_myDeleteElement = document.getElementById("svg_myDeleteElement");

    svg_myDrawElement.setAttribute("disabled", true);
    svg_myEditElement.removeAttribute("disabled");
    svg_myDeleteElement.removeAttribute("disabled");
}
function deleteElement() {
    var svg = document.getElementById("mySVG");
    svg.removeChild(svgSelectObject);
    svgSelectObject = null;
}
function editElement() {
    deleteElement();
    drawElement();
    setEditMode();
    svgSelectObject = null;
}
function resetButton() {
    var svg_myDrawElement = document.getElementById("svg_myDrawElement");
    var svg_myEditElement = document.getElementById("svg_myEditElement");
    var svg_myDeleteElement = document.getElementById("svg_myDeleteElement");

    svg_myDrawElement.removeAttribute("disabled");

    svg_myEditElement.setAttribute("disabled", true);
    svg_myDeleteElement.setAttribute("disabled", true);

}
//-----------------------------------------

//clear
function myClearSVC() {
    var svg = document.getElementById("mySVG");
    while (svg.firstChild) {
        svg.removeChild(svg.lastChild);
    }
}
function myClearValue() {
    var myDiv = document.getElementById("myDivFB");
    console.log(myDiv);
    inputs = myDiv.querySelectorAll("input[type=text]");
    for (i = 0; i < inputs.length; i++)
        inputs[i].value = '';

    selects = myDiv.querySelectorAll("select");
    for (i = 0; i < selects.length; i++)
        selects[i].value = '';
}
function myClearAll() {
    myClearSVC();
    myClearValue();
    svgSelectObject = null;
    svg_data_ID = 0;

}

//=========================================

function myOnChangeStandard() {

    drawOutLine();
}
function myOnChangeLeng() {
    drawOutLine();
}

//-----------------------------------------
//FB 사각형 그리기 버튼 클릭
function drawOutLine() {

    //SVG 및 input box Clear
    myClearSVC();

    //DOM 정보 읽기
    svg = document.getElementById("mySVG");
    svg_standard = document.getElementById("svg_standard").value;
    svg_submaterial = document.getElementById("svg_submaterial").value;
    svgWidth = document.getElementById("svg_leng").value;



    //입력이 없으면 종료
    if (!svg || !svg_standard || !svgWidth) return;

    //높이 두께 검출
    var arrSpec = svg_standard.split("*");
    if (arrSpec.length < 2) return;

    svgHeight = parseInt(arrSpec[0]);
    svgWidth = parseInt(svgWidth);
    svgThickness = parseInt(arrSpec[1].substr(0, arrSpec[1].length - 1));

    //디버깅
    console.log(svgNS);
    console.log(svg);
    console.log(svg_standard);
    console.log(arrSpec);

    drawOutLineSW();
}

function drawOutLineSW() {

    //FB 크기 다시 정의
    svg.setAttribute("width", svgWidth);
    svg.setAttribute("height", svgHeight);

    //FB 모양 그리기
    var rect = document.createElementNS(svgNS, 'rect');
    rect.setAttribute("x", 0);
    rect.setAttribute("y", 0);

    rect.setAttribute("width", svgWidth);
    rect.setAttribute("height", svgHeight);
    rect.setAttribute("style", "stroke-width:3px; stroke:#775577; fill:none");
    svg.appendChild(rect);
}


//=========================================


//사용지하 않음
function myOnChangeMacro() {
}
function myOnChangeA() {
}

//커팅그림 그리기 버튼 클릭
function drawElement() {

    //입력이 없으면 종료
    if (!svg || !svg_standard || !svgHeight || !svgWidth) {
        alert("기준정보(규격)가 입력되지 않았습니다.")
        return;
    }

    //DOM 정보
    var svg_dist = document.getElementById("svg_dist").value;
    var svg_macro = document.getElementById("svg_macro").value;
    var svg_A = document.getElementById("svg_A").value;

    //입력이 없으면
    if (!svg_dist) svg_dist = 0;
    if (!svg_macro) {
        alert("해당 매크로가 없습니다.");
        return;
    }
    if (!svg_A) svg_A = 0;

    svg_dist = parseInt(svg_dist);
    svg_A = parseInt(svg_A);
    drawElementSW(svg_macro, svg_A, svg_dist);
}
function drawElementSW(svg_macro, svg_A, svg_dist) {

    var svg_myDrawElement = document.getElementById("svg_myDrawElement");
    if (svg_myDrawElement)
        svg_myDrawElement.setAttribute("disabled", true);

    switch (svg_macro) {
        case 'FBP00':
            break;

        case 'FBP01':
            drawFBP01(svg_macro, svg_A, svg_dist);
            break;

        case 'FBP02':
            drawFBP02(svg_macro, svg_A, svg_dist);
            break;

        case 'FBP03':
            drawFBP03(svg_macro, svg_A, svg_dist);
            break;

        case 'FBP04':
            drawFBP04(svg_macro, svg_A, svg_dist);
            break;

        case 'FBP11':
            drawFBP11(svg_macro, svg_A, svg_dist);
            break;

        case 'FBP12':
            drawFBP12(svg_macro, svg_A, svg_dist);
            break;

        case 'FBP13':
            drawFBP13(svg_macro, svg_A, svg_dist);
            break;


        default:
            alert("해당 매크로가 없습니다.");
            break;
    }
    if (svg_myDrawElement)
        svg_myDrawElement.removeAttribute("disabled");
}

//-----------------------------------------

function drawFBP01(macro, A, dist) {
    //svgHeightTop, svgHeightBottom, svgThickness
    h = svgHeight;
    w = svgWidth;
    t = svgThickness;

    nW = 11;
    sH = 43;

    path = document.createElementNS(svgNS, "path");
    path = makeID8Event(path, macro, A, dist);
    pathValueA = "M " + (w - nW) + " " + 0
        + " L " + w + " " + parseInt((h - sH) / 2)
        + " L " + w + " " + parseInt(h - (h - sH) / 2)
        + " L " + (w - nW) + " " + h
        ;
    console.log(pathValueA);
    path.setAttribute("d",
        pathValueA
    );
    path.setAttribute("style", "fill:none; stroke:#3355ff; stroke-width:3;");
    svg.appendChild(path);


}
function drawFBP02(macro, A, dist) {
    //svgHeightTop, svgHeightBottom, svgThickness
    h = svgHeight;
    w = svgWidth;
    t = svgThickness;

    nW = 11;
    sH = 43;

    path = document.createElementNS(svgNS, "path");
    path = makeID8Event(path, macro, A, dist);
    pathValueA = "M " + nW + " " + 0
        + " L " + 0 + " " + parseInt((h - sH) / 2)
        + " L " + 0 + " " + parseInt(h - (h - sH) / 2)
        + " L " + nW + " " + h
        ;
    console.log(pathValueA);
    path.setAttribute("d",
        pathValueA
    );
    path.setAttribute("style", "fill:none; stroke:#3355ff; stroke-width:3;");
    svg.appendChild(path);
}
function drawFBP03(macro, A, dist) {
    //svgHeightTop, svgHeightBottom, svgThickness
    h = svgHeight;
    w = svgWidth;
    t = svgThickness;

    nW = 16;

    if (A <= 0) {
        alert("원의 반지름을 입력하세요.");
        return;
    }

    path = document.createElementNS(svgNS, "path");
    path = makeID8Event(path, macro, A, dist);
    pathValueA = "M " + (nW) + " " + 0
        + " L " + 0 + " " + parseInt((h - A) / 2)

        ////arch
        //// M 시작점x 시작점y
        //// A 가로R 세로R
        //// "x-rotation-degree" "large-arc-flag" "sweep-flag"
        //// 끝점x 끝점y

        + " A " + A + " " + A   //A는 원의 반지름
        + " " + 0 + " " + 0 + " " + 1
        + " " + 0 + " " + parseInt(h - ((h - A) / 2))

        + " L " + nW + " " + h
        ;
    console.log(pathValueA);
    path.setAttribute("d",
        pathValueA
    );
    path.setAttribute("style", "fill:none; stroke:#3355ff; stroke-width:3;");
    svg.appendChild(path);
}
function drawFBP04(macro, A, dist) {
    //svgHeightTop, svgHeightBottom, svgThickness
    h = svgHeight;
    w = svgWidth;
    t = svgThickness;

    r = parseInt(svgHeight / 2)

    path = document.createElementNS(svgNS, "path");
    path = makeID8Event(path, macro, A, dist);
    pathValueA = "M " + r + " " + 0

        ////arch
        //// M 시작점x 시작점y
        //// A 가로R 세로R
        //// "x-rotation-degree" "large-arc-flag" "sweep-flag"
        //// 끝점x 끝점y

        + " A " + r + " " + r
        + " " + 0 + " " + 1 + " " + 0
        + " " + r + " " + h
        ;
    console.log(pathValueA);
    path.setAttribute("d",
        pathValueA
    );
    path.setAttribute("style", "fill:none; stroke:#3355ff; stroke-width:3;");
    svg.appendChild(path);
}
function drawFBP11(macro, A, dist) {
    //svgHeightTop, svgHeightBottom, svgThickness
    h = svgHeight;
    w = svgWidth;
    t = svgThickness;

    len = 27;
    radianA = 45 * Math.PI / 180;
    tanB = parseInt(len * Math.cos(radianA));

    if (dist <= 0) {
        alert("가공할 간격(거리)을 입력하세요.");
        return;
    }

    path = document.createElementNS(svgNS, "path");
    path = makeID8Event(path, macro, A, dist);
    pathValueA = "M " + (dist) + " " + parseInt((h / 2) - tanB)
        + " L " + (dist + tanB) + " " + parseInt((h / 2))
        + " L " + (dist) + " " + parseInt((h / 2) + tanB)
        + " L " + (dist - tanB) + " " + parseInt((h / 2))
        + " L " + (dist) + " " + parseInt((h / 2) - tanB)
        ;
    console.log(pathValueA);
    path.setAttribute("d",
        pathValueA
    );
    path.setAttribute("style", "fill:none; stroke:#3355ff; stroke-width:3;");
    svg.appendChild(path);
}
function drawFBP12(macro, A, dist) {
    //svgHeightTop, svgHeightBottom, svgThickness
    h = svgHeight;
    w = svgWidth;
    t = svgThickness;

    r = 13;

    if (dist <= 0) {
        alert("가공할 간격(거리)을 입력하세요.");
        return;
    }

    circle = document.createElementNS(svgNS, "circle");
    circle = makeID8Event(circle, macro, A, dist);
    circle.setAttribute("cx", dist);
    circle.setAttribute("cy", parseInt(h / 2));
    circle.setAttribute("r", parseInt(r));//지름
    circle.setAttribute("style", "fill:none; stroke:#3355ff; stroke-width:3;");
    svg.appendChild(circle);
}
function drawFBP13(macro, A, dist) {
    //svgHeightTop, svgHeightBottom, svgThickness
    h = svgHeight;
    w = svgWidth;
    t = svgThickness;

    r = 11;

    if (dist <= 0) {
        alert("가공할 간격(거리)을 입력하세요.");
        return;
    }

    circle = document.createElementNS(svgNS, "circle");
    circle = makeID8Event(circle, macro, A, dist);
    circle.setAttribute("cx", dist);
    circle.setAttribute("cy", parseInt(h / 2));
    circle.setAttribute("r", parseInt(r));//지름
    circle.setAttribute("style", "fill:none; stroke:#3355ff; stroke-width:3;");
    svg.appendChild(circle);
}

//=========================================
function saveJSON() {
    var svg = document.getElementById("mySVG");
    objs = svg.children;

    var cutlistOBJs = [];
    for (var i = 0; i < objs.length; i++) {
        if (objs[i].nodeName == "rect") continue;

        //DOM정보 읽기
        //id="svg_id_5" name="svg_name_5" data-ID="5" data-dist="111" data-macro="FBP04" data-A="20"
        //{"CUT": ["가공거리", "매크로명", "Param1", "Param2", "Param3", "Param4", "Param5"]}
        let data_ID = objs[i].getAttribute("data-id");  //소문자 차리
        let data_dist = objs[i].getAttribute("data-dist");  //소문자 차리
        let data_macro = objs[i].getAttribute("data-macro");  //소문자 차리
        let data_A = objs[i].getAttribute("data-a");  //소문자 차리

        //값 없으면 설정
        if (!data_ID) data_ID = 0;
        if (!data_dist) data_dist = 0;
        if (!data_macro) data_macro = 0;
        if (!data_A) data_A = 0;
        data_B = 0;
        data_C = 0;
        data_D = 0;
        data_E = 0;

        //디버깅 출력
        console.log(data_ID);
        console.log(data_dist);
        console.log(data_macro);
        console.log(data_A);
        console.log("=================s ");

        var aObj = { "CUT": ["" + data_dist, "" + data_macro, "" + data_A, "" + data_B, "" + data_C, "" + data_D, "" + data_E] };
        cutlistOBJs.push(aObj);

    }//for

    //저장
    var cutlistDom = document.getElementById("id_cutlist");
    cutlistDom.value = JSON.stringify(cutlistOBJs);
}

function drawElementFromJSON() {
    //https://java119.tistory.com/54

    //get dome infor
    if (!svg)
        svg = document.getElementById("mySVG");

    var standard = document.getElementById("id_standard");
    var length_dwg = document.getElementById("id_length_dwg");

    console.log(standard);
    console.log(length_dwg);
    if (!standard || !length_dwg) {
        alert("FB 규격정보가 없습니다.");
        return;
    }


    svg_standard = standard.value;
    document.getElementById("svg_standard").value = svg_standard;
    document.getElementById("svg_leng").value = length_dwg.value;

    //높이 두께 검출
    var arrSpec = standard.value.split("*");
    if (arrSpec.length < 2) return;

    svgHeight = parseInt(arrSpec[0]);
    svgWidth = parseInt(length_dwg.value);
    svgThickness = parseInt(arrSpec[1].substr(0, arrSpec[1].length - 1));
    drawOutLineSW();

    var cutlistDom = document.getElementById("id_cutlist");

    var cutlistJson = JSON.parse(cutlistDom.value);
    cutlistJson.forEach(element => {
        console.log(element.CUT[0]);
        console.log(element.CUT[1]);
        console.log(element.CUT[2]);
        console.log(element.CUT[3]);
        console.log(element.CUT[4]);
        console.log(element.CUT[5]);
        console.log(element.CUT[6]);
        console.log("================");

        //{"CUT": ["가공거리", "매크로명", "Param1", "Param2", "Param3", "Param4", "Param5"]}
        svg_dist = parseInt(element.CUT[0]);
        svg_macro = element.CUT[1];
        svg_A = parseInt(element.CUT[2]);

        if (!svg_dist) svg_dist = 0;
        if (!svg_A) svg_A = 0;

        drawElementSW(svg_macro, svg_A, svg_dist)
    });
}


//=========================================


//테스트 코드
function myTestAddJson() {

    //https://java119.tistory.com/54
    var cutlistDom = document.getElementById("id_cutlist");
    var cutlistJson = JSON.parse(cutlistDom.value);

    var aJson = { "ID": 99, "CUT": ["가공거리", "매크로명", "Param441", "Param442", "Param443", "Param444", "Param445"] };
    cutlistJson.push(aJson);

    cutlistJson.forEach(element => {
        console.log(element.ID, element.CUT)
    });


    cutlistDom.value = JSON.stringify(cutlistJson);
    return;
}


document.addEventListener("DOMContentLoaded", function () {
    if(document.getElementById("id_standard"))
        drawElementFromJSON();
    else
        lastRun();
});
