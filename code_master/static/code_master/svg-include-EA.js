//임시 저장 관련 전역변수 사용경우 확인

var svgNS = "http://www.w3.org/2000/svg";
var svg = null;
var ttexture = null;
var ttype = null;
var tstandard = null;

var svgHeightTop = 0;
var svgHeightBottom = 0;
var svgHeight = 0;
var svgWidth = 0;
var thickness = 0;
var tmacro = null;

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

//-----------------------------------------

function myClearSVC() {
    var svg = document.getElementById("mySVG");
    while (svg.firstChild) {
        svg.removeChild(svg.lastChild);
    }
}

function myClearValue() {
    var myDiv = document.getElementById("myDIV");
    inputs = myDiv.querySelectorAll("input");
    for (i = 0; i < inputs.length; i++)
        inputs[i].value = '';

    selects = myDiv.querySelectorAll("select");
    for (i = 0; i < selects.length; i++)
        selects[i].value = '';
}

function myClearAll() {
    myClearSVC();
    myClearValue();
}

//-----------------------------------------
function myOnChangeTexture() {
    drawOutLine();
}

function myOnChangeType() {
    drawOutLine();
}

function myOnChangeStandard() {
    drawOutLine();
}

function myOnChangeLeng() {
    drawOutLine();
}

function drawOutLine() {
    myClearSVC();

    svg = document.getElementById("mySVG");
    ttexture = document.getElementById("ttexture").value;
    ttype = document.getElementById("ttype").value;
    tstandard = document.getElementById("tstandard").value;
    svgWidth = document.getElementById("leng").value;

    console.log(svgNS);
    console.log(svg);
    console.log(ttexture);
    console.log(ttype);
    console.log(tstandard);

    if (!svg || !ttype || !tstandard || !svgWidth) return;

    var arrSpec = tstandard.split("*");
    if (arrSpec.length < 3) return;


    svgHeightTop = parseInt(arrSpec[0]);
    svgHeightBottom = parseInt(arrSpec[1]);
    thickness = parseInt(arrSpec[2].substr(0, arrSpec[2].length - 1));

    console.log(arrSpec);
    console.log(svgHeightTop);
    console.log(svgHeightBottom);

    svgHeight = svgHeightTop + svgHeightBottom;
    //svgWidth = (svgHeightTop + svgHeightBottom) * 4;
    svgWidth = parseInt(svgWidth);


    svg.setAttribute("width", svgWidth);
    svg.setAttribute("height", svgHeight);

    switch (ttype) {
        case 'UA':
        case 'EA':
            var rectTop = document.createElementNS(svgNS, 'rect');
            rectTop.setAttribute("x", 0);
            rectTop.setAttribute("y", 0);

            rectTop.setAttribute("width", svgWidth);
            rectTop.setAttribute("height", svgHeightTop);
            rectTop.setAttribute("style", "stroke-width:1px; stroke:#26b2a2; fill:none");
            svg.appendChild(rectTop);

            var rectBottom = document.createElementNS(svgNS, 'rect');
            rectBottom.setAttribute("x", 0);
            rectBottom.setAttribute("y", svgHeightTop);

            rectBottom.setAttribute("width", svgWidth);
            rectBottom.setAttribute("height", svgHeightBottom);
            rectBottom.setAttribute("style", "stroke-width:1px; stroke:#26b2a2; fill:none");
            svg.appendChild(rectBottom);
            break;

        case 'CH':
            break;

        case 'HB':
            break;

        case 'IB':
            break;

        case 'PI':
            break;

        case 'SP':
            break;

        default:
            alert("해당 타입이 없습니다.");
            break;
    }
}

//-----------------------------------------

function myOnChangeMacro() {
}
function myOnChangeA() {
}
function myOnChangeB() {
}
function myOnChangeC() {
}
function myOnChangeD() {
}
function myOnChangeE() {
}

function drawElement() {
    console.log(svg);
    console.log(ttype);
    console.log(tstandard);
    console.log(svgHeightTop);
    console.log(svgHeightBottom);
    console.log(svgHeight);
    console.log(svgWidth);
    if (!svg || !ttype || !tstandard
        || !svgHeightTop || !svgHeightBottom
        || !svgHeight || !svgWidth) {
        console.log(ttype, tstandard, svgHeightTop, svgHeightBottom, svgHeight, svgWidth);
        alert("기준정보(타입, 규격)가 입력되지 않았습니다.")
        return;
    }

    var myDrawElement = document.getElementById("myDrawElement");
    var tmacro = document.getElementById("tmacro").value;
    var A = document.getElementById("A").value;
    var B = document.getElementById("B").value;
    var C = document.getElementById("C").value;
    var D = document.getElementById("D").value;
    var E = document.getElementById("E").value;
    console.log(tmacro);
    console.log("A:" + A);
    console.log("B:" + B);
    console.log("C:" + C);
    console.log("D:" + D);
    console.log("E:" + E);
    if (!tmacro || !A) {
        alert("해당 매크로가 없습니다.");
        return;
    }

    switch (ttype) {
        case 'UA':
        case 'EA':
            switch (tmacro) {

                case 'EA001':
                    if (!A || !B) return;
                    myDrawElement.setAttribute("disabled", true);
                    drawEA001(A, B, C, D, E);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA002':
                    if (!A || !B) return;
                    myDrawElement.setAttribute("disabled", true);
                    drawEA002(A, B, C, D, E);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA003':
                    if (!A || !B || !C || !D) return;
                    myDrawElement.setAttribute("disabled", true);
                    drawEA003(A, B, C, D, E);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA004':
                    if (!A || !B || !C) return;
                    myDrawElement.setAttribute("disabled", true);
                    drawEA004(A, B, C, D, E);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA005':
                    if (!A || !B || !C) return;
                    myDrawElement.setAttribute("disabled", true);
                    drawEA005(A, B, C, D, E);
                    myDrawElement.removeAttribute("disabled");
                    break;

                case 'EA101':
                    if (!A || !B) return;
                    myDrawElement.setAttribute("disabled", true);
                    drawEA101(A, B, C, D, E);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA102':
                    if (!A || !B) return;
                    myDrawElement.setAttribute("disabled", true);
                    drawEA102(A, B, C, D, E);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA103':
                    if (!A || !B || !C || !D) return;
                    myDrawElement.setAttribute("disabled", true);
                    drawEA103(A, B, C, D, E);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA104':
                    if (!A || !B || !C) return;
                    myDrawElement.setAttribute("disabled", true);
                    drawEA104(A, B, C, D, E);
                    myDrawElement.removeAttribute("disabled");
                    break;
                //-------------------------
                case 'EA021':
                    if (!A || !B) return;
                    myDrawElement.setAttribute("disabled", true);
                    drawEA021(A, B, C, D, E);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA022':
                    if (!A || !B) return;
                    myDrawElement.setAttribute("disabled", true);
                    drawEA022(A, B, C, D, E);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA023':
                    if (!A || !B || !C || !D) return;
                    myDrawElement.setAttribute("disabled", true);
                    drawEA023(A, B, C, D, E);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA024':
                    if (!A || !B || !C) return;
                    myDrawElement.setAttribute("disabled", true);
                    drawEA024(A, B, C, D, E);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA025':
                    if (!A || !B || !C) return;
                    myDrawElement.setAttribute("disabled", true);
                    drawEA025(A, B, C, D, E);
                    myDrawElement.removeAttribute("disabled");
                    break;

                case 'EA121':
                    if (!A || !B) return;
                    myDrawElement.setAttribute("disabled", true);
                    drawEA121(A, B, C, D, E);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA122':
                    if (!A || !B) return;
                    myDrawElement.setAttribute("disabled", true);
                    drawEA122(A, B, C, D, E);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA123':
                    if (!A || !B || !C || !D) return;
                    myDrawElement.setAttribute("disabled", true);
                    drawEA123(A, B, C, D, E);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA124':
                    if (!A || !B || !C) return;
                    myDrawElement.setAttribute("disabled", true);
                    drawEA124(A, B, C, D, E);
                    myDrawElement.removeAttribute("disabled");
                    break;
                //------------------------- check dist
                case 'EA011':
                    var dist = document.getElementById("dist").value;
                    if (!A || !B || !dist) {
                        return;
                    }
                    dist = parseInt(dist);

                    myDrawElement.setAttribute("disabled", true);
                    drawEA011(A, B, C, D, E, dist);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA111':
                    var dist = document.getElementById("dist").value;
                    if (!A || !B || !dist) {
                        return;
                    }
                    dist = parseInt(dist);

                    myDrawElement.setAttribute("disabled", true);
                    drawEA111(A, B, C, D, E, dist);
                    myDrawElement.removeAttribute("disabled");
                    break;

                case 'EA013':
                    dist = document.getElementById("dist").value;
                    if (!A || !B || !C || !dist) return;
                    dist = parseInt(dist);

                    myDrawElement.setAttribute("disabled", true);
                    drawEA013(A, B, C, D, E, dist);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA014':
                    dist = document.getElementById("dist").value;
                    if (!A || !B || !C || !dist) return;
                    dist = parseInt(dist);

                    myDrawElement.setAttribute("disabled", true);
                    drawEA014(A, B, C, D, E, dist);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA015':
                    dist = document.getElementById("dist").value;
                    if (!A || !dist) return;
                    dist = parseInt(dist);

                    myDrawElement.setAttribute("disabled", true);
                    drawEA015(A, B, C, D, E, dist);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA016':
                    dist = document.getElementById("dist").value;
                    if (!A || !B || !dist) return;
                    dist = parseInt(dist);

                    myDrawElement.setAttribute("disabled", true);
                    drawEA016(A, B, C, D, E, dist);
                    myDrawElement.removeAttribute("disabled");
                    break;

                case 'EA113':
                    dist = document.getElementById("dist").value;
                    if (!A || !B || !C || !dist) return;
                    dist = parseInt(dist);

                    myDrawElement.setAttribute("disabled", true);
                    drawEA113(A, B, C, D, E, dist);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA114':
                    dist = document.getElementById("dist").value;
                    if (!A || !B || !C || !dist) return;
                    dist = parseInt(dist);

                    myDrawElement.setAttribute("disabled", true);
                    drawEA114(A, B, C, D, E, dist);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA115':
                    dist = document.getElementById("dist").value;
                    if (!A || !dist) return;
                    dist = parseInt(dist);

                    myDrawElement.setAttribute("disabled", true);
                    drawEA115(A, B, C, D, E, dist);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA116':
                    dist = document.getElementById("dist").value;
                    if (!A || !B || !dist) return;
                    dist = parseInt(dist);

                    myDrawElement.setAttribute("disabled", true);
                    drawEA116(A, B, C, D, E, dist);
                    myDrawElement.removeAttribute("disabled");
                    break;
                //-------------------------

                case 'EA031':
                    dist = document.getElementById("dist").value;
                    if (!A || !B || !dist) return;
                    dist = parseInt(dist);

                    myDrawElement.setAttribute("disabled", true);
                    drawEA031(A, B, C, D, E, dist);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA032':
                    dist = document.getElementById("dist").value;
                    if (!A || !B ||!dist) return;
                    dist = parseInt(dist);

                    myDrawElement.setAttribute("disabled", true);
                    drawEA032(A, B, C, D, E, dist);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA033':
                    dist = document.getElementById("dist").value;
                    if (!A || !B || !C || !dist) return;
                    dist = parseInt(dist);

                    myDrawElement.setAttribute("disabled", true);
                    drawEA033(A, B, C, D, E, dist);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA034':
                    dist = document.getElementById("dist").value;
                    if (!A || !B || !C || !dist) return;
                    dist = parseInt(dist);

                    myDrawElement.setAttribute("disabled", true);
                    drawEA034(A, B, C, D, E, dist);
                    myDrawElement.removeAttribute("disabled");
                    break;


                case 'EA131':
                    dist = document.getElementById("dist").value;
                    if (!A || !B || !dist) return;
                    dist = parseInt(dist);

                    myDrawElement.setAttribute("disabled", true);
                    drawEA131(A, B, C, D, E, dist);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA132':
                    dist = document.getElementById("dist").value;
                    if (!A || !B || !dist) return;
                    dist = parseInt(dist);

                    myDrawElement.setAttribute("disabled", true);
                    drawEA132(A, B, C, D, E, dist);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA133':
                    dist = document.getElementById("dist").value;
                    if (!A || !B || !C || !dist) return;
                    dist = parseInt(dist);

                    myDrawElement.setAttribute("disabled", true);
                    drawEA133(A, B, C, D, E, dist);
                    myDrawElement.removeAttribute("disabled");
                    break;
                case 'EA134':
                    dist = document.getElementById("dist").value;
                    if (!A || !B || !C || !dist) return;
                    dist = parseInt(dist);

                    myDrawElement.setAttribute("disabled", true);
                    drawEA134(A, B, C, D, E, dist);
                    myDrawElement.removeAttribute("disabled");
                    break;
                default:
                    alert("해당 매크로가 없습니다.");
                    break;
            }
            break;
        default:
            alert("해당 타입이 없습니다.");
            break;
    }
}

function drawEA001(A, B, C, D, E) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    if (parseInt(B) > svgHeightTop) {
        alert("높이의 값이 엥글의 날보다 큽니다.")
        return;
    }
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + A + " " + 0
        + " L " + 0 + " " + B
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    path.setAttribute("onclick", "alert(this.id );");
    path.setAttribute("id", "path_01");
    svg.appendChild(path);

}
function drawEA002(A, B, C, D, E) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    if (parseInt(B) > svgHeightTop) {
        alert("높이의 값이 엥글의 날보다 큽니다.")
        return;
    }
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + A + " " + 0
        + " L " + A + " " + B
        + " L " + 0 + " " + B
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);
}
function drawEA003(A, B, C, D, E) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + B + " " + 0
        + " L " + A + " " + (svgHeightTop + parseInt(C))
        + " L " + D + " " + (svgHeightTop + parseInt(C))
        + " L " + 0 + " " + (svgHeightTop + parseInt(C) + parseInt(D))
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);
}
function drawEA004(A, B, C, D, E) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + A + " " + 0
        + " L " + 0 + " " + B
        + " L " + C + " " + svgHeightTop
        + " L " + C + " " + (svgHeightTop + svgHeightBottom)
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);
}
function drawEA005(A, B, C, D, E) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + A + " " + 0
        + " L " + B + " " + svgHeightTop
        + " L " + C + " " + h
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);
}
function drawEA101(A, B, C, D, E) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + A + " " + (h)
        + " L " + 0 + " " + (h - parseInt(B))
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);
}
function drawEA102(A, B, C, D, E) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + A + " " + (h)
        + " L " + A + " " + (h - parseInt(B))
        + " L " + 0 + " " + (h - parseInt(B))
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);
}
function drawEA103(A, B, C, D, E) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + B + " " + h
        + " L " + A + " " + (h - (svgHeightBottom + parseInt(C)))
        + " L " + D + " " + (h - (svgHeightBottom + parseInt(C)))
        + " L " + 0 + " " + (h - (svgHeightBottom + parseInt(C) + parseInt(D)))
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);
}
function drawEA104(A, B, C, D, E) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + A + " " + h
        + " L " + 0 + " " + (h - parseInt(B))
        + " L " + C + " " + svgHeightTop
        + " L " + C + " " + 0
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);
}
//-------------------------
function drawEA021(A, B, C, D, E) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    if (parseInt(B) > svgHeightTop) {
        alert("높이의 값이 엥글의 날보다 큽니다.")
        return;
    }
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + (w - parseInt(A)) + " " + 0
        + " L " + (w) + " " + B
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);

}
function drawEA022(A, B, C, D, E) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    if (parseInt(B) > svgHeightTop) {
        alert("높이의 값이 엥글의 날보다 큽니다.")
        return;
    }
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + (w - parseInt(A)) + " " + 0
        + " L " + (w - parseInt(A)) + " " + B
        + " L " + w + " " + B
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);
}
function drawEA023(A, B, C, D, E) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + (w - parseInt(B)) + " " + 0
        + " L " + (w - parseInt(A)) + " " + (svgHeightTop + parseInt(C))
        + " L " + (w - parseInt(D)) + " " + (svgHeightTop + parseInt(C))
        + " L " + w + " " + (svgHeightTop + parseInt(C) + parseInt(D))
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);
}
function drawEA024(A, B, C, D, E) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + (w - parseInt(A)) + " " + 0
        + " L " + w + " " + B
        + " L " + (w - parseInt(C)) + " " + svgHeightTop
        + " L " + (w - parseInt(C)) + " " + (svgHeightTop + svgHeightBottom)
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);
}
function drawEA025(A, B, C, D, E) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + (w - parseInt(A)) + " " + 0
        + " L " + (w - parseInt(B)) + " " + svgHeightTop
        + " L " + (w - parseInt(C)) + " " + h
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);
}
function drawEA121(A, B, C, D, E) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + (w - parseInt(A)) + " " + (h)
        + " L " + w + " " + (h - parseInt(B))
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);
}
function drawEA122(A, B, C, D, E) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + (w - parseInt(A)) + " " + (h)
        + " L " + (w - parseInt(A)) + " " + (h - parseInt(B))
        + " L " + w + " " + (h - parseInt(B))
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);
}
function drawEA123(A, B, C, D, E) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    console.log('drawEA123');
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + (w - parseInt(B)) + " " + h
        + " L " + (w - parseInt(A)) + " " + (h - (svgHeightBottom + parseInt(C)))
        + " L " + (w - parseInt(D)) + " " + (h - (svgHeightBottom + parseInt(C)))
        + " L " + w + " " + (h - (svgHeightBottom + parseInt(C) + parseInt(D)))
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);
}
function drawEA124(A, B, C, D, E) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + (w - parseInt(A)) + " " + h
        + " L " + w + " " + (h - parseInt(B))
        + " L " + (w - parseInt(C)) + " " + svgHeightTop
        + " L " + (w - parseInt(C)) + " " + 0
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);
}
//-------------------------

function drawEA011(A, B, C, D, E, dist) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;

    console.log(A, B, C, dist);
    circle = document.createElementNS(svgNS, "circle");
    circle.setAttribute("cx", dist);
    circle.setAttribute("cy", B);
    circle.setAttribute("r", parseInt(A / 2));//지름
    circle.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");

    svg.appendChild(circle);
}
function drawEA111(A, B, C, D, E, dist) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;

    console.log(A, B, C, dist);
    circle = document.createElementNS(svgNS, "circle");
    circle.setAttribute("cx", dist);
    circle.setAttribute("cy", (h - parseInt(B)));
    circle.setAttribute("r", parseInt(A / 2));//지름
    circle.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");

    svg.appendChild(circle);
}

function drawEA013(A, B, C, D, E, dist) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;

    //arch
    pathA = document.createElementNS(svgNS, "path");
    // M시작점x 시작점y 
    // A가로R 세로R 
    // "x-rotation-degree" "large-arc-flag" "sweep-flag"
    // 끝점x 끝점y
    pathValueA = "M " + (dist - parseInt(C) / 2) + " " + (parseInt(B) - parseInt(A) / 2)
        + " A " + (parseInt(A) / 2) + " " + (parseInt(A) / 2)
        + " " + 0 + " " + 1 + " " + 0
        + (dist - parseInt(C) / 2) + " " + (parseInt(B) + parseInt(A) / 2)
        ;
    console.log(pathValueA);
    pathA.setAttribute("d",
        pathValueA
    );
    pathA.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(pathA);


    pathB = document.createElementNS(svgNS, "path");
    // M시작점x 시작점y 
    // A가로R 세로R 
    // "x-rotation-degree" "large-arc-flag" "sweep-flag"
    // 끝점x 끝점y
    pathValueB = "M " + (dist + parseInt(C) / 2) + " " + (parseInt(B) - parseInt(A) / 2)
        + " A " + (parseInt(A) / 2) + " " + (parseInt(A) / 2)
        + " " + 0 + " " + 1 + " " + 1
        + (dist + parseInt(C) / 2) + " " + (parseInt(B) + parseInt(A) / 2)
        ;
    console.log(pathValueB);
    pathB.setAttribute("d",
        pathValueB
    );
    pathB.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(pathB);

    //lineA
    pathA = document.createElementNS(svgNS, "path");
    pathValueA = "M " + (dist - parseInt(C) / 2) + " " + (parseInt(B) - parseInt(A) / 2)
        + " L " + (dist + parseInt(C) / 2) + " " + (parseInt(B) - parseInt(A) / 2)
        ;
    console.log(pathValueA);
    pathA.setAttribute("d",
        pathValueA
    );
    pathA.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(pathA);

    //lineB
    pathB = document.createElementNS(svgNS, "path");
    pathValueB = "M " + (dist - parseInt(C) / 2) + " " + (parseInt(B) + parseInt(A) / 2)
        + " L " + (dist + parseInt(C) / 2) + " " + (parseInt(B) + parseInt(A) / 2)
        ;
    console.log(pathValueB);
    pathB.setAttribute("d",
        pathValueB
    );
    pathB.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(pathB);
}
function drawEA014(A, B, C, D, E, dist) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;

    //arch
    pathA = document.createElementNS(svgNS, "path");
    // M시작점x 시작점y 
    // A가로R 세로R 
    // "x-rotation-degree" "large-arc-flag" "sweep-flag"
    // 끝점x 끝점y
    pathValueA = "M " + (dist - parseInt(A) / 2) + " " + (parseInt(B) - parseInt(C) / 2)
        + " A " + (parseInt(A) / 2) + " " + (parseInt(A) / 2)
        + " " + 0 + " " + 1 + " " + 1
        + (dist + parseInt(A) / 2) + " " + (parseInt(B) - parseInt(C) / 2)
        ;
    console.log(pathValueA);
    pathA.setAttribute("d",
        pathValueA
    );
    pathA.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(pathA);


    pathB = document.createElementNS(svgNS, "path");
    // M시작점x 시작점y 
    // A가로R 세로R 
    // "x-rotation-degree" "large-arc-flag" "sweep-flag"
    // 끝점x 끝점y
    pathValueB = "M " + (dist - parseInt(A) / 2) + " " + (parseInt(B) + parseInt(C) / 2)
        + " A " + (parseInt(A) / 2) + " " + (parseInt(A) / 2)
        + " " + 0 + " " + 1 + " " + 0
        + (dist + parseInt(A) / 2) + " " + (parseInt(B) + parseInt(C) / 2)
        ;
    console.log(pathValueB);
    pathB.setAttribute("d",
        pathValueB
    );
    pathB.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(pathB);

    //lineA
    pathA = document.createElementNS(svgNS, "path");
    pathValueA = "M " + (dist - parseInt(A) / 2) + " " + (parseInt(B) - parseInt(C) / 2)
        + " L " + (dist - parseInt(A) / 2) + " " + (parseInt(B) + parseInt(C) / 2)
        ;
    console.log(pathValueA);
    pathA.setAttribute("d",
        pathValueA
    );
    pathA.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(pathA);

    //lineB
    pathB = document.createElementNS(svgNS, "path");
    pathValueB = "M " + (dist + parseInt(A) / 2) + " " + (parseInt(B) - parseInt(C) / 2)
        + " L " + (dist + parseInt(A) / 2) + " " + (parseInt(B) + parseInt(C) / 2)
        ;
    console.log(pathValueB);
    pathB.setAttribute("d",
        pathValueB
    );
    pathB.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(pathB);
}
function drawEA015(A, B, C, D, E, dist) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    var radianA = parseInt(A) * Math.PI / 180;

    tanD = Math.tan(radianA) * svgHeightTop; //x길이

    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + (dist - tanD) + " " + 0
        + " L " + dist + " " + (svgHeightTop - thickness)   //주의 두께만큼 차감
        + " L " + (dist + tanD) + " " + 0
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);
}
function drawEA016(A, B, C, D, E, dist) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + dist + " " + 0
        + " L " + dist + " " + B
        + " L " + (dist + parseInt(A)) + " " + B
        + " L " + (dist + parseInt(A)) + " " + 0
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);
}

function drawEA113(A, B, C, D, E, dist) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;

    //arch
    pathA = document.createElementNS(svgNS, "path");
    // M시작점x 시작점y 
    // A가로R 세로R 
    // "x-rotation-degree" "large-arc-flag" "sweep-flag"
    // 끝점x 끝점y
    pathValueA = "M " + (dist - parseInt(C) / 2) + " " + (h - (parseInt(B) + parseInt(A) / 2))
        + " A " + (parseInt(A) / 2) + " " + (parseInt(A) / 2)
        + " " + 0 + " " + 1 + " " + 0
        + (dist - parseInt(C) / 2) + " " + (h - (parseInt(B) - parseInt(A) / 2))
        ;
    console.log(pathValueA);
    pathA.setAttribute("d",
        pathValueA
    );
    pathA.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(pathA);


    pathB = document.createElementNS(svgNS, "path");
    // M시작점x 시작점y 
    // A가로R 세로R 
    // "x-rotation-degree" "large-arc-flag" "sweep-flag"
    // 끝점x 끝점y
    pathValueB = "M " + (dist + parseInt(C) / 2) + " " + (h - (parseInt(B) + parseInt(A) / 2))
        + " A " + (parseInt(A) / 2) + " " + (parseInt(A) / 2)
        + " " + 0 + " " + 1 + " " + 1
        + (dist + parseInt(C) / 2) + " " + (h - (parseInt(B) - parseInt(A) / 2))
        ;
    console.log(pathValueB);
    pathB.setAttribute("d",
        pathValueB
    );
    pathB.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(pathB);

    //lineA
    pathA = document.createElementNS(svgNS, "path");
    pathValueA = "M " + (dist - parseInt(C) / 2) + " " + (h - (parseInt(B) + parseInt(A) / 2))
        + " L " + (dist + parseInt(C) / 2) + " " + (h - (parseInt(B) + parseInt(A) / 2))
        ;
    console.log(pathValueA);
    pathA.setAttribute("d",
        pathValueA
    );
    pathA.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(pathA);

    //lineB
    pathB = document.createElementNS(svgNS, "path");
    pathValueB = "M " + (dist - parseInt(C) / 2) + " " + (h - (parseInt(B) - parseInt(A) / 2))
        + " L " + (dist + parseInt(C) / 2) + " " + (h - (parseInt(B) - parseInt(A) / 2))
        ;
    console.log(pathValueB);
    pathB.setAttribute("d",
        pathValueB
    );
    pathB.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(pathB);
}
function drawEA114(A, B, C, D, E, dist) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;

    //arch
    pathA = document.createElementNS(svgNS, "path");
    // M시작점x 시작점y 
    // A가로R 세로R 
    // "x-rotation-degree" "large-arc-flag" "sweep-flag"
    // 끝점x 끝점y
    pathValueA = "M " + (dist - parseInt(A) / 2) + " " + (h - (parseInt(B) + parseInt(C) / 2))
        + " A " + (parseInt(A) / 2) + " " + (parseInt(A) / 2)
        + " " + 0 + " " + 1 + " " + 1
        + (dist + parseInt(A) / 2) + " " + (h - (parseInt(B) + parseInt(C) / 2))
        ;
    console.log(pathValueA);
    pathA.setAttribute("d",
        pathValueA
    );
    pathA.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(pathA);


    pathB = document.createElementNS(svgNS, "path");
    // M시작점x 시작점y 
    // A가로R 세로R 
    // "x-rotation-degree" "large-arc-flag" "sweep-flag"
    // 끝점x 끝점y
    pathValueB = "M " + (dist - parseInt(A) / 2) + " " + (h - (parseInt(B) - parseInt(C) / 2))
        + " A " + (parseInt(A) / 2) + " " + (parseInt(A) / 2)
        + " " + 0 + " " + 1 + " " + 0
        + (dist + parseInt(A) / 2) + " " + (h - (parseInt(B) - parseInt(C) / 2))
        ;
    console.log(pathValueB);
    pathB.setAttribute("d",
        pathValueB
    );
    pathB.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(pathB);

    //lineA
    pathA = document.createElementNS(svgNS, "path");
    pathValueA = "M " + (dist - parseInt(A) / 2) + " " + (h - (parseInt(B) + parseInt(C) / 2))
        + " L " + (dist - parseInt(A) / 2) + " " + (h - (parseInt(B) - parseInt(C) / 2))
        ;
    console.log(pathValueA);
    pathA.setAttribute("d",
        pathValueA
    );
    pathA.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(pathA);

    //lineB
    pathB = document.createElementNS(svgNS, "path");
    pathValueB = "M " + (dist + parseInt(A) / 2) + " " + (h - (parseInt(B) + parseInt(C) / 2))
        + " L " + (dist + parseInt(A) / 2) + " " + (h - (parseInt(B) - parseInt(C) / 2))
        ;
    console.log(pathValueB);
    pathB.setAttribute("d",
        pathValueB
    );
    pathB.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(pathB);
}
function drawEA115(A, B, C, D, E, dist) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    var radianA = parseInt(A) * Math.PI / 180;

    tanD = Math.tan(radianA) * svgHeightTop; //x길이

    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + (dist - tanD) + " " + h
        + " L " + dist + " " + (svgHeightTop + thickness)   //주의 두께만큼 차감
        + " L " + (dist + tanD) + " " + h
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);
}
function drawEA116(A, B, C, D, E, dist) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + dist + " " + h
        + " L " + dist + " " + (h - B)
        + " L " + (dist + parseInt(A)) + " " + (h - B)
        + " L " + (dist + parseInt(A)) + " " + h
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);
}

//-------------------------

function drawEA031(A, B, C, D, E, dist) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    if (parseInt(B) > svgHeightTop) {
        alert("높이의 값이 엥글의 날보다 큽니다.")
        return;
    }
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + dist + " " + B
        + " L " + (dist + parseInt(A)) + " " + B
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);

}
function drawEA032(A, B, C, D, E, dist) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    if (parseInt(B) > svgHeightTop) {
        alert("높이의 값이 엥글의 날보다 큽니다.")
        return;
    }
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + dist + " " + B
        + " L " + dist + " " + (parseInt(B) + parseInt(A))
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);

}
function drawEA033(A, B, C, D, E, dist) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    if (parseInt(B) > svgHeightTop) {
        alert("높이의 값이 엥글의 날보다 큽니다.")
        return;
    }
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + dist + " " + (parseInt(B) + parseInt(C))
        + " L " + (dist + parseInt(A)) + " " + B
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);

}
function drawEA034(A, B, C, D, E, dist) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    if (parseInt(B) > svgHeightTop) {
        alert("높이의 값이 엥글의 날보다 큽니다.")
        return;
    }
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + dist + " " + B
        + " L " + (dist + parseInt(A)) + " " + (parseInt(B) + parseInt(C))
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);

}


function drawEA131(A, B, C, D, E, dist) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    if (parseInt(B) > svgHeightTop) {
        alert("높이의 값이 엥글의 날보다 큽니다.")
        return;
    }
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + dist + " " + (h - parseInt(B))
        + " L " + (dist + parseInt(A)) + " " + (h - parseInt(B))
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);

}
function drawEA132(A, B, C, D, E, dist) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    if (parseInt(B) > svgHeightTop) {
        alert("높이의 값이 엥글의 날보다 큽니다.")
        return;
    }
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + dist + " " + (h - (parseInt(B) + parseInt(A)))
        + " L " + dist + " " + (h - parseInt(B))
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);

}
function drawEA133(A, B, C, D, E, dist) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    if (parseInt(B) > svgHeightTop) {
        alert("높이의 값이 엥글의 날보다 큽니다.")
        return;
    }
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + dist + " " + (h - (parseInt(B)))
        + " L " + (dist + parseInt(A)) + " " + (h - (parseInt(B) + parseInt(C)))
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);

}
function drawEA134(A, B, C, D, E, dist) {
    //svgHeightTop, svgHeightBottom
    h = svgHeightTop + svgHeightBottom;
    w = svgWidth;
    if (parseInt(B) > svgHeightTop) {
        alert("높이의 값이 엥글의 날보다 큽니다.")
        return;
    }
    path = document.createElementNS(svgNS, "path");
    pathValue = "M " + dist + " " + (h - (parseInt(B) + parseInt(C)))
        + " L " + (dist + parseInt(A)) + " " + (h - parseInt(B))
        ;
    console.log(pathValue);
    path.setAttribute("d",
        pathValue
    );
    path.setAttribute("style", "fill:none; stroke:#26b2a2; stroke-width:2;");
    svg.appendChild(path);

}



function test() {

    var svg = document.getElementById("mySVG");
    console.log(svg);
    var svgNS = "http://www.w3.org/2000/svg";

    //이 값을 변경해보면서
    var groupCount = 2;


    var totlaCount = 0;

    var width = 800;
    var height = 600;
    var size = 30;
    var tab = 20;

    var axp = 0;
    var ayp = 0;
    var awidth = 0;
    var aheight = 0;
    var aradius = 0;
    var atab = 0;
    var afill = 0;



    var startTime = new Date().getTime();

    for (var i = 0; i < groupCount; i++) {

        var middleStartTime = new Date().getTime();

        //===============================================
        var countR = getRandomNumber(0, 10);
        console.log("count(rect): " + countR);
        for (var j = 0; j < countR; j++) {
            axp = getRandomNumber(0, width);
            ayp = getRandomNumber(0, height);
            awidth = getRandomNumber(5, size);
            aheight = getRandomNumber(5, size);
            aradius = getRandomNumber(5, size);
            atab = getRandomNumber(10, tab);
            afill = getRandomColor();

            var rect = document.createElementNS(svgNS, 'rect');
            rect.setAttribute('x', axp);
            rect.setAttribute('y', ayp);
            rect.setAttribute('width', awidth);
            rect.setAttribute('height', aheight);
            rect.setAttribute('fill', afill);
            rect.setAttribute('style', 'stroke: black;');
            svg.appendChild(rect);
        }//for j

        //===============================================
        var countC = getRandomNumber(0, 10);
        console.log("count(circle): " + countC);
        for (var j = 0; j < countC; j++) {
            axp = getRandomNumber(0, width);
            ayp = getRandomNumber(0, height);
            awidth = getRandomNumber(5, size);
            aheight = getRandomNumber(5, size);
            aradius = getRandomNumber(5, size);
            atab = getRandomNumber(10, tab);
            afill = getRandomColor();

            var circle = document.createElementNS(svgNS, 'circle');
            circle.setAttribute('cx', axp);
            circle.setAttribute('cy', ayp);
            circle.setAttribute('r', aradius);
            circle.setAttribute('fill', afill);
            circle.setAttribute('style', 'stroke: black;');
            svg.appendChild(circle);


        }//for j

        //===============================================
        var countP = getRandomNumber(0, 10);
        console.log("count(path): " + countP);
        for (var j = 0; j < countP; j++) {
            axp = getRandomNumber(0, width);
            ayp = getRandomNumber(0, height);
            awidth = getRandomNumber(5, size);
            aheight = getRandomNumber(5, size);
            aradius = getRandomNumber(5, size);
            atab = getRandomNumber(10, tab);
            afill = getRandomColor();

            var path = document.createElementNS(svgNS, 'path');
            path.setAttribute('d',
                "M " +
                axp + " " +
                ayp + " " +

                " C " +
                (axp + atab) + " " +
                (ayp - atab) + " " +

                (axp + atab * 2) + " " +
                (ayp - atab) + " " +

                (axp + atab * 3) + " " +
                ayp + " " +

                " S " +
                (axp + atab * 4) + " " +
                (ayp + atab) + " " +

                (axp + atab * 6) + " " +
                ayp + " "
            );
            path.setAttribute('style', 'stroke:' + afill + '; fill:none; stroke-width:6px; stroke-linecap:round;');
            svg.appendChild(path);



        }//for j

        //===============================================
        var countT = getRandomNumber(0, 10);
        console.log("count(text): " + countT);
        for (var j = 0; j < countT; j++) {
            axp = getRandomNumber(0, width);
            ayp = getRandomNumber(0, height);
            awidth = getRandomNumber(5, size);
            aheight = getRandomNumber(5, size);
            aradius = getRandomNumber(5, size);
            atab = getRandomNumber(10, tab);
            afill = getRandomColor();

            var svgTxt = document.createElementNS(svgNS, 'text');
            svgTxt.setAttribute('x', axp);
            svgTxt.setAttribute('y', ayp);
            //svgTxt.setAttribute('r', aradius);
            //svgTxt.setAttribute('fill', afill);
            svgTxt.setAttribute('style', 'stroke: ' + afill + '; fill: none; font-size:' + atab + 'px;');
            var svgTxtString = document.createTextNode('Hello SHS');
            svgTxt.appendChild(svgTxtString);
            svg.appendChild(svgTxt);



        }//for j

        var middleEndTime = new Date().getTime();

        console.log(totlaCount + "ea, " + "1 cycle time: " + (middleEndTime - middleStartTime) / 1000);
        console.log("accumulate time: " + (middleEndTime - startTime) / 1000);

    }//for i
    var endTIme = new Date().getTime();
    console.log("whole " + totlaCount + "ea, " + "time: " + (endTIme - startTime) / 1000);

}



