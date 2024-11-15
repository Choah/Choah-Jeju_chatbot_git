import streamlit as st
import streamlit.components.v1 as components
import os

# Set the default search keyword from a file, if it exists
base_dir = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(base_dir, "data/location.txt"), "r", encoding="utf-8") as file:
        search_keyword = file.read().strip()
except FileNotFoundError:
    search_keyword = "제주"

# HTML and JavaScript for the Kakao Maps interface
html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>키워드로 장소검색하고 목록으로 표출하기</title>
    <style>
        .map_wrap, .map_wrap * {margin:0;padding:0;font-family:'Malgun Gothic',dotum,'돋움',sans-serif;font-size:12px;}
        .map_wrap {position:relative;width:100%;height:500px;}
        #menu_wrap {position:absolute;top:0;left:0;bottom:0;width:250px;margin:10px 0 30px 10px;padding:5px;overflow-y:auto;background:rgba(255, 255, 255, 0.7);z-index: 1;font-size:12px;border-radius: 10px;}
        #placesList li {list-style: none;}
        #placesList .item {position:relative;border-bottom:1px solid #888;overflow: hidden;cursor: pointer;min-height: 65px;}
        #pagination {margin:10px auto;text-align: center;}
        #pagination a {display:inline-block;margin-right:10px;}
    </style>
</head>
<body>
    <div class="map_wrap">
        <div id="map" style="width:100%;height:500px;"></div>
        <div id="menu_wrap">
            <div class="option">
                <form onsubmit="searchPlaces(); return false;">
                    키워드: <input type="text" id="keyword" value="제주" size="15"> 
                    <button type="submit">검색하기</button> 
                </form>
            </div>
            <hr>
            <ul id="placesList"></ul>
            <div id="pagination"></div>
        </div>
    </div>

    <script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey=28e4d4739fe65a650ce5cb32cf39e00e&libraries=services"></script>
    <script>
        var mapContainer = document.getElementById('map');
        var mapOption = {
            center: new kakao.maps.LatLng(33.49962, 126.531188),
            level: 3
        };
        var map = new kakao.maps.Map(mapContainer, mapOption);
        var ps = new kakao.maps.services.Places();
        var infowindow = new kakao.maps.InfoWindow({zIndex:1});

        function searchPlaces() {
            var keyword = document.getElementById('keyword').value;
            if (!keyword.replace(/^\s+|\s+$/g, '')) {
                alert('키워드를 입력해주세요!');
                return false;
            }
            ps.keywordSearch(keyword, placesSearchCB);
        }

        function placesSearchCB(data, status, pagination) {
            if (status === kakao.maps.services.Status.OK) {
                displayPlaces(data);
            } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
                alert('검색 결과가 존재하지 않습니다.');
            } else if (status === kakao.maps.services.Status.ERROR) {
                alert('검색 결과 중 오류가 발생했습니다.');
            }
        }

        function displayPlaces(places) {
            var listEl = document.getElementById('placesList'),
                fragment = document.createDocumentFragment(),
                bounds = new kakao.maps.LatLngBounds();

            removeAllChildNods(listEl);

            for (var i=0; i<places.length; i++) {
                var placePosition = new kakao.maps.LatLng(places[i].y, places[i].x),
                    itemEl = getListItem(i, places[i]);
                bounds.extend(placePosition);

                (function(lat, lng) {
                    itemEl.onclick = function() {
                        sendCoordinates(lat, lng);
                    };
                })(places[i].y, places[i].x);

                fragment.appendChild(itemEl);
            }
            listEl.appendChild(fragment);
            map.setBounds(bounds);
        }

        function getListItem(index, places) {
            var el = document.createElement('li');
            el.innerHTML = '<div class="info"><h5>' + places.place_name + '</h5></div>';
            el.className = 'item';
            return el;
        }

        function sendCoordinates(lat, lng) {
            const coordinates = {latitude: lat, longitude: lng};
            const streamlitEvent = new CustomEvent("sendCoordinates", {detail: coordinates});
            window.parent.document.dispatchEvent(streamlitEvent);
        }

        function removeAllChildNods(el) {
            while (el.hasChildNodes()) {
                el.removeChild(el.lastChild);
            }
        }
    </script>
</body>
</html>
"""