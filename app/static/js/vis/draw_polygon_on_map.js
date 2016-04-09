$(document).ready(function(){
  // TODO this part should be done byusing get request
  // get the color from get request from the server
  var inputJson;

  // set up the canvas size
  var cellWidth = 10;
  var cellHeight = 10;

  // canvas col and row num
  var dataX;
  var dataY;
  // original veg code
  var vegOrigin;
  // current veg code
  var vegCurrent;
  // elevation information for all HRU cells
  var elevationInfo;

  var canvasWidth;
  var canvasHeight;
  var canvasHandle;
  var canvas2DContext;

  // this is for define color for the cells
  var colorScale;

  // record the chosen area rec top left
  var firstPoint = {x:-1,y:-1};
  // record the chosen area rec bot right
  var secondPoint = {x:-1,y:-1};
  // record mouse click time
  var clickTime = 0;

  // this var record all the chosen HRU num
  var chosenHRU = [];
  // this struct array records chosen HRU and color
  // [{colorInfo:'#ffffff',HRUInfo:[1,2,3]},{...}]
  var chosenAreaInfo = [];

  // define google map with map
  var map;
  // this is for image overlay
  var imgOverlay;
  var imageBounds;
  // url for overlay image
  var imgURL;

  // this is for mouse dragging
  var isDragging = false;
  var isMousePressing = false;
  var firstPosition;
  var secondPosition;

  // this part is for the fire simulation
  // this record the fire border
  var fireBorder = [];
  // each element in this array should  be [cellNumber, vegType, burnTime, r]
  // r = vegTransferRateCurrent*wind/cos(slope)
  // if r >= 1  then spread fire, if r <= 0, r = 0
  // r contains 8 elements, because the basic 8 fire grid system
  var onfireCell = [];
  // this array only records array cell num
  var onfireCellNum = [];
  // different veg should burn last different amount of time
  // I used fake data here until chao find real one
  var vegBurnTime = [0, 1, 2, 3, 4];
  // different veg should have different fire pass rate
  // fire pass from one area to another
  // e.g. gress is easier to pass fire to other areas
  // scale down from paper data: 0, 3955, 70, 2533
  // no data for conifers, use the same as trees
  var vegTransferRate = [0, 1, 0.0182, 0.6405, 0.6405];
  // the eight elements should be between 0 and 1
  // the eight elements are 
  // west-north, north, north-east, west,
  // east, south-west, south, east-south
  // all the elements should be between 0 and 2, en... just to control speed
  // need more scientific wind model
  var wind = [1,2,1,1,1,1,1,1];




  $.get('/api/base-veg-map', function(data){
    inputJson = data;

    // grab col and row num
    dataX = inputJson['projection_information']['ncol'];
    dataY = inputJson['projection_information']['nrow'];

    vegOrigin = obtainJsoninto1D(inputJson);
    elevationInfo = inputJson['elevation'].slice();
    var minElevation = elevationInfo.min();
    var maxElevation = elevationInfo.max();
    // append input area and instruction
    // this part should be dynamically generated
    $("#elevationInputID").append("<p>The elevation scale is from "+minElevation.toString()+" to "+maxElevation.toString()+"</p>");
    $("#elevationInputID").append("<input type='number' min='"+minElevation.toString()+"' max='"+maxElevation.toString()+"' step='0.1' id='elevationSelectorID'>");
    $("#elevationInputID").append("<input type='button' class='btn btn-sm btn-sm-map' id='confirmElevationButton' value='Update Map by Elevation' />");

    // should not use var vegCurrent = vegOrigin
    // coz when we change vegCurrent and then vegOrigin will change too
    vegCurrent = vegOrigin.slice();

    canvasWidth = cellWidth*dataX;
    canvasHeight = cellHeight*dataY;
    // I am so confusing at this part...
    // If I change it into $('.mapCanvas').css('width',canvasWidth.toString()+'px');
    // then it only draw 30 boxes each line
    $('.mapCanvas').attr('width',canvasWidth.toString()+'px');
    $('.mapCanvas').attr('height',canvasHeight.toString()+'px');

    // place mapArray into canvas
    canvasHandle = document.getElementById("myCanvas");
    //var canvas2DContext = [];
    canvas2DContext = canvasHandle.getContext("2d");

    // this is for define color for the cells
    //var scaleSize = Object.size(inputJson['vegetation_map']);
    var scaleSize = 5;
    //colorScale = chroma.scale(['pink','black','blue','red','green']).colors(scaleSize);
    colorScale = chroma.scale(['white','#003300']).colors(scaleSize);
    // add fire color to be the last element
    colorScale.push('#FF0000');
    // this part is used to push data into canvas
    // and paint color
    resetCanvas(vegOrigin);

    // overlay canvas on google map
    var latLonInformation = inputJson['projection_information'];
    // TODO map overlay works correctly
    overlayCanvasonGoogleMap(latLonInformation['xllcorner'],
        latLonInformation['xurcorner'],
        latLonInformation['yllcorner'],
        latLonInformation['yurcorner']);



    $("#myCanvas")
    .mousedown(function(evt){
      isMousePressing = true;
    })
    .mousemove(function(evt){
      // record the first mouse position
      if(isDragging==false && isMousePressing==true)
      {
        // start point
        clickTime = 1;
        firstPosition = getMousePos(canvasHandle, evt);
        isDragging = true;
        changeCanvasCellColor(firstPosition,"#FFFF00");
      }
      else if(isDragging == true && isMousePressing==true)
      {
        clickTime = 2;
        secondPosition = getMousePos(canvasHandle, evt);
        changeCanvasCellColor(secondPosition,"#FFFF00");
      }
    })
    .mouseup(function(evt){
      isMousePressing = false;
      // choose single cell
      if(isDragging==false)
      {
        clickTime = 1;
        firstPosition = getMousePos(canvasHandle, evt);
        changeCanvasCellColor(firstPosition,"#FF00FF");
        secondPosition = firstPosition;
        clickTime = 2;
        changeCanvasCellColor(secondPosition,"#FF00FF");
      }
      // choose an area
      else if(isDragging==true)
      {
        isDragging = false;
      }
       // push the final chosen area into chosenAreaInfo
      // get the current chosen color number
      var colorOptNum = parseInt($('#vegetation-type-selector label.active input').val());
            //parseInt($('input[name="vegcode-select"]:checked').val());
      chosenAreaInfo.push({colorNum:colorOptNum,chosenArea:chosenHRU});
      chosenHRU=[];
    });

    $('#confirmElevationButton').click(function(){
      changeVegByElevation(vegCurrent, elevationInfo, dataX, dataY);

      resetCanvas(vegCurrent);

      // update map overlay
      updateMapOverlay();
    });


    $("#resetCanvasButton").click(function(){
      resetCanvas(vegOrigin);
      vegCurrent = vegOrigin.slice();
      clickTime = 0;
      chosenHRU = [];
      chosenArea = [];

      fireBorder = [];
      onfireCell = [];
      onfireCellNum = [];
  
      updateMapOverlay();
    });

    $("#save-veg-update").click(function(){

      $.each(chosenAreaInfo, function(index1, value1) {
        //var tempColor = value1.colorNum;
        $.each(value1.chosenArea,function(index2,value2){

          vegCurrent[value2] = value1.colorNum;

        });
      });

      chosenAreaInfo = [];

      resetCanvas(vegCurrent);

      // update map overlay
      updateMapOverlay();
    });

    $("#fireModeID").click(function(){


      $.each(chosenAreaInfo, function(index1, value1) {
        //var tempColor = value1.colorNum;
        $.each(value1.chosenArea,function(index2,value2){
          // this if prevent duplicate elements to be pushed
          if($.inArray(value2, onfireCellNum) === -1)
          {
            // cell num, veg type, burn time
            onfireCell.push([value2, vegCurrent[value2], 0, [0,0,0,0,0,0,0,0]]);
            onfireCellNum.push(value2);

            // the last element is for fire color
            vegCurrent[value2] = colorScale.length - 1;  
          }
          
        });
      });

      resetCanvas(vegCurrent);

      // update map overlay
      updateMapOverlay();
      // call startFire() every half second
      setInterval(startFire, 500);
    });

    $("#submitChangetoServerButton").click(function(){
      // update json file based on the current HRU values
      updateJson();
      //var jsonStr = JSON.stringify(inputJson);
      $.ajax({
          type : "POST",
          url : "/api/base-veg-map",
          data: JSON.stringify(inputJson, null, '\t'),
          contentType: 'application/json;charset=UTF-8',
          success: function(result) {
          }
      });

    });


    $("#removeOverlayButton").click(function(){
      removeOverlay();
    });

    $("#addOverlayButton").click(function(){
      addOverlay();
    });

    $("#changeOpacityButton").click(function(){
      changeOverlayOpacity();
    });


  });



  // this is used to find the length of an obj
  // this is from http://stackoverflow.com/questions/5223/length-of-a-javascript-object-that-is-associative-array
  Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
  };

  // this function is used to change json based on vegCurrent
  function updateJson()
  {
    var hruNum;
    var vegType;
    var objSize = Object.size(inputJson['vegetation_map']);
    // this for loop is for initialize the JSON HRU part
    for(var i=0; i<objSize; i++)
    {
      inputJson['vegetation_map'][i.toString()]['HRU_number'] = [];
    }

    // modify JSON HRU part
    for(var m=0 ; m<dataY ; m++)
      {
        for(var i=0 ; i<dataX ; i++)
        {
          hruNum = i + m*dataX;
          vegType = vegCurrent[hruNum];
          inputJson['vegetation_map'][vegType.toString()]['HRU_number'].push(hruNum);
        }
      }
  }


  // this function grab data json input and create a 1D array of hru values
  function obtainJsoninto1D(inputJson)
  {
    var totalHRUNum = 0;

    var outputArr = new Array(dataX*dataY);
    // for this case veg_code is the loop count (from 0), vegCode is str
    // therefore veg_code = i.toString()
    var tempSize;
    $.each(['bare_ground', 'grasses', 'shrubs', 'trees', 'conifers'],
      function(i, cov_type) {
        tempSize = inputJson[cov_type].length;
        totalHRUNum = totalHRUNum + tempSize;
        for(var m=0; m<tempSize; m++ )
        {
          outputArr[inputJson[cov_type][m]] = i;
        }
      }
    );
    // test if the inputJson is valid
    if(totalHRUNum == dataX*dataY)
    {
      return outputArr;  
    }
    else
    {
      console.log('Data from the get request is not right.');
      console.log('HRU number is not consistent.');
      return [];
    }
    
  }

  // this is from http://www.html5canvastutorials.com/advanced/html5-canvas-mouse-coordinates/
  // get the mouse position, based on px
  function getMousePos(canvas, evt)
  {
    var rect = canvas.getBoundingClientRect();
    return {
      x: evt.clientX - rect.left,
      y: evt.clientY - rect.top
    };
  }

  // this function is used to refresh canvas with the original veg code
  function resetCanvas(colorMatrix)
  {
      for(var m=0 ; m<dataY ; m++)
      {
        for(var i=0 ; i<dataX ; i++)
        {
          canvas2DContext.fillStyle = colorScale[colorMatrix[i+dataX*m]];
          //                          start x,     y,            width,    height
          canvas2DContext.fillRect(cellWidth*i,cellHeight*m,cellWidth,cellHeight);
          // draw lines to separate cell
          canvas2DContext.rect(cellWidth*i,cellHeight*m,cellWidth,cellHeight);
        }
      }
      canvas2DContext.stroke();
  }

  // this function only reset fire place
  function resetFireCanvas(inputOnfireCellNum)
  {
    // m is for y
    // i is for x
    var m;
    var i;

    $.each(inputOnfireCellNum,function(index, value){
      m = Math.floor(value / dataX);
      i = Math.floor(value % dataX);
      // not bare ground
      if(onfireCell[index][1] != 0)
      {
        // the last element is for fire color
        canvas2DContext.fillStyle = colorScale[colorScale.length - 1];
      }
      // bare ground
      else
      {
        canvas2DContext.fillStyle = colorScale[0];
      }
      //                          start x,     y,            width,    height
      canvas2DContext.fillRect(cellWidth*i,cellHeight*m,cellWidth,cellHeight);
      // draw lines to separate cell
      canvas2DContext.rect(cellWidth*i,cellHeight*m,cellWidth,cellHeight);
    });

    canvas2DContext.stroke();
  }

  // this function requires top left and bot right points for the chosen area
  function showChosenRecArea(input1,input2)
  {
    var p1 = {x:input1.x,y:input1.y};
    var p2 = {x:input2.x,y:input2.y};
    var temp;
    canvas2DContext.fillStyle = "#FFFF00";
    // not the same point
    if(p2.x!=p1.x&&p2.y!=p1.y)
    {
      if(p2.x < p1.x)
      {
        temp = p2.x;
        p2.x = p1.x;
        p1.x = temp;
      }
      if(p2.y < p1.y)
      {
        temp = p2.y;
        p2.y = p1.y;
        p1.y = temp;
      }
      // Here +1 coz need to count the bottom line too
      canvas2DContext.fillRect(p1.x*cellWidth, p1.y*cellHeight, cellWidth*(p2.x-p1.x+1), cellHeight*(p2.y-p1.y+1));
    }
    // two points in the same column
    else if(p2.x==p1.x&&p2.y!=p1.y)
    {
      if(p2.y < p1.y)
      {
        temp = p2.y;
        p2.y = p1.y;
        p1.y = temp;
      }
      // Here +1 coz need to count the bottom line too
      canvas2DContext.fillRect(p1.x*cellWidth, p1.y*cellHeight, cellWidth, cellHeight*(p2.y-p1.y+1));
    }
    // two points in the same row
    else if(p2.x!=p1.x&&p2.y==p1.y)
    {
      if(p2.x < p1.x)
      {
        temp = p2.x;
        p2.x = p1.x;
        p1.x = temp;
      }
      // Here +1 coz need to count the bottom line too
      canvas2DContext.fillRect(p1.x*cellWidth, p1.y*cellHeight, cellWidth*(p2.x-p1.x+1), cellHeight);
    }
    // choose the single cell
    else if(p2.x==p1.x&&p2.y==p1.y)
    {
      canvas2DContext.fillRect(p1.x*cellWidth, p1.y*cellHeight, cellWidth, cellHeight);
    }
    // push chosen HRU cell num
    recordChosenAreaInfo(p1,p2);

  }

  // this function is used to add the chosen cell number into chosenHRU
  // for this function p1.x and p1.y should be =< p2.x and p2.y
  // after this function chosenHRU may have some duplicated elements
  function recordChosenAreaInfo(p1,p2)
  {
    // get the current chosen color number
    // var colorOptNum =
    //       parseInt($('input[name="vegcode-select"]:checked').val());

    // single point
    if(p1.x==p2.x && p1.y==p2.y)
    {
      chosenHRU.push(p1.x+p2.y*dataX);
    }
    else
    {
      for(var m=p1.y; m<=p2.y; m++)
      {
        for(var i=p1.x; i<=p2.x; i++)
        {
          chosenHRU.push(i+m*dataX);
        }
      }
    }

  }

  function changeCanvasCellColor(mousePosition,color)
  {
    var startX = Math.floor(mousePosition.x/cellWidth);
    var startY = Math.floor(mousePosition.y/cellHeight);
    canvas2DContext.fillStyle = color;
    canvas2DContext.fillRect(startX*cellWidth, startY*cellHeight, cellWidth, cellHeight);

    if(clickTime == 1)
    {
      firstPoint.x = startX;
      firstPoint.y = startY;
    }
    else if(clickTime == 2)
    {
      secondPoint.x = startX;
      secondPoint.y = startY;

      showChosenRecArea(firstPoint,secondPoint);

    }

  }

  Array.prototype.max = function() {
    return Math.max.apply(null, this);
  };

  Array.prototype.min = function() {
    return Math.min.apply(null, this);
  };

  function changeVegByElevation(inputHRU, inputElevationInfo, inputArrX, inputArrY)
  {
    var hruNum = 0;
    var elevationThreshold = $('#elevationSelectorID').val();
    // get the current chosen color number
    var colorOptNum = parseInt($('#vegetation-type-selector label.active input').val());

    for(var m=0 ; m<inputArrY ; m++)
    {
      for(var i=0 ; i<inputArrX ; i++)
      {
        hruNum = i + m*dataX;
        if(inputElevationInfo[hruNum] >= elevationThreshold)
        {
          inputHRU[hruNum] = colorOptNum;
        }
      }
    }
  }

  function startFire()
  {

    // spread fire
    // parallel.js should go here!!!!!!!!!!!!!
    $.each(onfireCellNum,function(index, value){

      spreadFire(value,dataX,dataY,index);

      var burnMaxtime = vegBurnTime[onfireCell[index][1]];
      // if not bare ground, the cell can burn
      if(onfireCell[index][1] != 0)
      {
        if(onfireCell[index][2] <= burnMaxtime)
        {
          onfireCell[index][2] = onfireCell[index][2] + 1;
        }
        else
        {
          // change it into bare ground if cell is burn out
          onfireCell[index][1] = 0;
        }
      }
    });
      
    resetFireCanvas(onfireCellNum);

    // update map overlay
    updateMapOverlay();
  }

  function spreadFire(firePos, maxX, maxY,fireCellIndex)
  {
    // only is current cell is not bare ground
    // the fire will spread
    if(onfireCell[fireCellIndex][1] != 0)
    {
      
      if(firePos == 0)
      {
        // right
        fireRight(firePos,fireCellIndex);
        // right bot
        fireRightBot(firePos,fireCellIndex);
        // down
        fireBot(firePos,fireCellIndex);     
      }
      else if(firePos == (maxX-1))
      {
        // down
        fireBot(firePos,fireCellIndex);
        // down left
        fireLeftBot(firePos,fireCellIndex);
        // left
        fireLeft(firePos,fireCellIndex);
      }
      // first row, not corners
      else if(firePos>0 && firePos<(maxX-1))
      {
       // right
        fireRight(firePos,fireCellIndex);
        // right bot
        fireRightBot(firePos,fireCellIndex);
        // down
        fireBot(firePos,fireCellIndex);
        // down left
        fireLeftBot(firePos,fireCellIndex);
        // left
        fireLeft(firePos,fireCellIndex);
      }
      // left most column and not top left corner and not bot left corner
      else if(firePos%maxX==0 && Math.floor(firePos/maxX)!=(maxY-1) && firePos!=0)
      {
        fireTop(firePos,fireCellIndex);
        fireBot(firePos,fireCellIndex);
        fireRightBot(firePos,fireCellIndex);
        fireRight(firePos,fireCellIndex);
        fireRightTop(firePos,fireCellIndex);
      }
      // bot left corner
      else if(firePos%maxX==0 && Math.floor(firePos/maxX)==(maxY-1))
      {
        fireTop(firePos,fireCellIndex);
        fireRight(firePos,fireCellIndex);
        fireRightTop(firePos,fireCellIndex);
      }
      // bot right corner
      else if((firePos+1)%maxX==0 && ((firePos+1)/maxX)==maxY)
      {
        fireTop(firePos,fireCellIndex);
        fireLeft(firePos,fireCellIndex);
        fireLeftTop(firePos,fireCellIndex);
      }
      // right most column and not top right corner and not bot right corner
      else if((firePos+1)%maxX==0 && ((firePos+1)/maxX)!=maxY && firePos!=(maxX-1))
      {
        fireTop(firePos,fireCellIndex);
        fireBot(firePos,fireCellIndex);
        fireLeft(firePos,fireCellIndex);
        fireLeftBot(firePos,fireCellIndex);
        fireLeftTop(firePos,fireCellIndex);
      }
      // last row, not corners
      else if(firePos%maxX!=0 && Math.floor(firePos/maxX)==(maxY-1) && (firePos+1)%maxX!=0)
      {
        fireRight(firePos,fireCellIndex);
        fireRightTop(firePos,fireCellIndex);
        fireLeftTop(firePos,fireCellIndex);
        fireLeft(firePos,fireCellIndex);
        fireTop(firePos,fireCellIndex);
      }
      // not at the border line
      else if(firePos%maxX!=0 && Math.floor(firePos/maxX)<(maxY-1) && Math.floor(firePos/maxX)>0 && (firePos+1)%maxX!=0)
      {
        fireTop(firePos,fireCellIndex);
        fireBot(firePos,fireCellIndex);
        fireLeft(firePos,fireCellIndex);
        fireRight(firePos,fireCellIndex);
        fireLeftBot(firePos,fireCellIndex);
        fireLeftTop(firePos,fireCellIndex);
        fireRightBot(firePos,fireCellIndex);
        fireRightTop(firePos,fireCellIndex);
      }
    }

    function updateFireArray(tempIndex)
    {

      var elementPos = onfireCellNum.indexOf(tempIndex);
      // not in array and not bare ground
      if(elementPos==-1)
      {
        onfireCellNum.push(tempIndex);
        onfireCell.push([tempIndex, vegCurrent[tempIndex], 0, [0,0,0,0,0,0,0,0]]);
        //vegCurrent[tempIndex] = colorScale.length - 1;
      }
      // if in the on fire array and not bare ground
      // update burning time
      // else if(elementPos!=-1 && onfireCell[elementPos][1]!=0)
      // {
      //   var burnMaxtime = vegBurnTime[onfireCell[elementPos][1]];
      //   if(onfireCell[elementPos][2] <= burnMaxtime)
      //   {
      //     onfireCell[elementPos][2] = onfireCell[elementPos][2] + 1;
      //   }
      //   else
      //   {
      //     // change it into bare ground if cell is burn out
      //     onfireCell[elementPos][1] = 0;
      //   }
      // }
    }
    // right top, left top, left bot, and right bot have longer recLong
    function getCos(centerCellIndex,aimCellIndex,isLonger)
    {
      var deltaHeight  = Math.abs(elevationInfo[centerCellIndex]-elevationInfo[centerCellIndex]);
      if(!isLonger)
      {
        // 10000 is 100*100, 100 is grid length
        var recLong = Math.sqrt(10000+(deltaHeight*deltaHeight));
        return 100/recLong;
      }
      else
      {
        // sqrt(20000) is grid length
        var recLong = Math.sqrt(20000+(deltaHeight*deltaHeight));
        return Math.sqrt(20000)/recLong;
      }
      
    }

    function fireTop(inputIndex,inputFireCellIndex)
    {
      var longer = false;
      var cosValue = getCos(inputIndex,(inputIndex-maxX),longer);
      var rveg = wind[1]*vegTransferRate[onfireCell[inputFireCellIndex][1]]/cosValue;
      onfireCell[inputFireCellIndex][3][1] += rveg;
      if(onfireCell[inputFireCellIndex][3][1] >= 1)
      {
        inputIndex = inputIndex - maxX;
  
        updateFireArray(inputIndex);
      }
      else if(onfireCell[inputFireCellIndex][3][1] <= 0)
      {
        onfireCell[inputFireCellIndex][3][1] = 0;
      }

    }

    function fireRightTop(inputIndex,inputFireCellIndex)
    {
      var longer = true;
      var cosValue = getCos(inputIndex,(inputIndex - maxX + 1),longer);
      var rveg = wind[2]*vegTransferRate[onfireCell[inputFireCellIndex][1]]/cosValue;
      onfireCell[inputFireCellIndex][3][2] += rveg;
      if(onfireCell[inputFireCellIndex][3][2] >= 1)
      {
        inputIndex = inputIndex - maxX + 1;

        updateFireArray(inputIndex);
      }
      else if(onfireCell[inputFireCellIndex][3][2] <= 0)
      {
        onfireCell[inputFireCellIndex][3][2] = 0;
      }      

    }

    function fireRight(inputIndex,inputFireCellIndex)
    {
      var longer = false;
      var cosValue = getCos(inputIndex,(inputIndex + 1),longer);
      var rveg = wind[4]*vegTransferRate[onfireCell[inputFireCellIndex][1]]/cosValue;
      onfireCell[inputFireCellIndex][3][4] += rveg;
      if(onfireCell[inputFireCellIndex][3][4] >= 1)
      {
        // right
        inputIndex = inputIndex + 1;

        updateFireArray(inputIndex);
      }
      else if(onfireCell[inputFireCellIndex][3][4] <= 0)
      {
        onfireCell[inputFireCellIndex][3][4] = 0;
      }

    }

    function fireRightBot(inputIndex,inputFireCellIndex)
    {
      var longer = true;
      var cosValue = getCos(inputIndex,(inputIndex + maxX),longer);
      var rveg = wind[7]*vegTransferRate[onfireCell[inputFireCellIndex][1]]/cosValue;
      onfireCell[inputFireCellIndex][3][7] += rveg;
      if(onfireCell[inputFireCellIndex][3][7] >= 1)
      {
        inputIndex = inputIndex + maxX;

        updateFireArray(inputIndex);
      }
      else if(onfireCell[inputFireCellIndex][3][7] <= 0)
      {
        onfireCell[inputFireCellIndex][3][7] = 0;
      }      

    }

    function fireBot(inputIndex,inputFireCellIndex)
    {
      var longer = false;
      var cosValue = getCos(inputIndex,(inputIndex + maxX),longer);
      var rveg = wind[6]*vegTransferRate[onfireCell[inputFireCellIndex][1]]/cosValue;
      onfireCell[inputFireCellIndex][3][6] += rveg;
      if(onfireCell[inputFireCellIndex][3][6] >= 1)
      {
        inputIndex = inputIndex + maxX;

        updateFireArray(inputIndex);
      }
      else if(onfireCell[inputFireCellIndex][3][6] <= 0)
      {
        onfireCell[inputFireCellIndex][3][6] = 0;
      }

    }

    function fireLeftBot(inputIndex,inputFireCellIndex)
    {
      var longer = true;
      var cosValue = getCos(inputIndex,(inputIndex + maxX - 1),longer);
      var rveg = wind[5]*vegTransferRate[onfireCell[inputFireCellIndex][1]]/cosValue;
      onfireCell[inputFireCellIndex][3][5] += rveg;
      if(onfireCell[inputFireCellIndex][3][5] >= 1)
      {
        inputIndex = inputIndex + maxX - 1;

        updateFireArray(inputIndex);
      }
      else if(onfireCell[inputFireCellIndex][3][5] <= 0)
      {
        onfireCell[inputFireCellIndex][3][5] = 0;
      }


    }

    function fireLeftTop(inputIndex,inputFireCellIndex)
    {
      var longer = true;
      var cosValue = getCos(inputIndex,(inputIndex - maxX - 1),longer);
      var rveg = wind[0]*vegTransferRate[onfireCell[inputFireCellIndex][1]]/cosValue;
      onfireCell[inputFireCellIndex][3][0] += rveg;
      if(onfireCell[inputFireCellIndex][3][0] >= 1)
      {
        inputIndex = inputIndex - maxX - 1;

        updateFireArray(inputIndex);
      }
      else if(onfireCell[inputFireCellIndex][3][0] <= 0)
      {
        onfireCell[inputFireCellIndex][3][0] = 0;
      }

    }


    function fireLeft(inputIndex,inputFireCellIndex)
    {
      var longer = false;
      var cosValue = getCos(inputIndex,(inputIndex - 1),longer);
      var rveg = wind[3]*vegTransferRate[onfireCell[inputFireCellIndex][1]]/cosValue;
      onfireCell[inputFireCellIndex][3][3] += rveg;
      if(onfireCell[inputFireCellIndex][3][3] >= 1)
      {
        inputIndex = inputIndex - 1;

        updateFireArray(inputIndex);
      }
      else if(onfireCell[inputFireCellIndex][3][3] <= 0)
      {
        onfireCell[inputFireCellIndex][3][3] = 0;
      }


    }

  }

});
