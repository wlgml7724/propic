
  $(document).ready(function(){
        var albumSlideList = $(".main_album .album_slide .slide_list");
        var albumSlideListLi = $(".main_album .album_slide .slide_list .btn_link");
        var albumCloneLen = Math.ceil(13 / albumSlideListLi.length);
        var albumSlideClone = albumSlideListLi.clone();
        for(var i=0; i<albumCloneLen; i++) {
            albumSlideList.append(albumSlideClone);
        }
        var getAlbumList = albumSlideList.find(".btn_link").slice(-6);
        albumSlideList.prepend(getAlbumList);
        
        var albumMargin = 212;
        var albumMarginLeft = 114;
        var albumMarginRight = 228;
        $(".main_album .album_slide .slide_list .btn_link").each(function(i) {
            var getAlbumLeft = i * albumMargin;
            if(i==6) getAlbumLeft += albumMarginLeft;
            else if(i>6) getAlbumLeft += albumMarginRight;
            $(this).css("left", getAlbumLeft);
        });
        
        var albumCheck = true;
        var getAlbumIdx = $(".main_album .album_slide .slide_list .btn_link").eq(6).addClass("active zoom").data("index");
        //앨번 슬라이드
        var mainAlbumSlide = $(".main_album .album_list").removeClass("load").bxSlider({
            mode:"fade",
            auto:false,
            pause:4000,
            speed:300,
            pager:false,
            controls:false,
            startSlide:parseInt(getAlbumIdx, 10)
        });
        
        setTimeout(function() {
            var albumSlide = $(".main_album .album_slide").addClass("load");
            
            $(".main_album .album_slide .slide_list").on("click", ".btn_link", function() {
                if($(this).hasClass("active")) {
                    return true;
                }
                else if(albumCheck == true) {
                    albumCheck = false;
                    var getActive = $(".main_album .album_slide .slide_list .btn_link.active");
                    var getIdx = getActive.index();
                    var getNext = $(this);
                    var getNextIdx = getNext.index();
                    var getMoveIdx = 0;
                    if(getNextIdx > getIdx) {
                        getMoveIdx = getNextIdx - getIdx;
                        var getMove = $(".main_album .album_slide .slide_list .btn_link").slice(0, getMoveIdx);
                        var getMoveClone = getMove.clone();
                        getMove.remove();
                        albumSlideList.append(getMoveClone);
                    }
                    else {
                        getMoveIdx = -(getIdx - getNextIdx);
                        var getMove = $(".main_album .album_slide .slide_list .btn_link").slice(getMoveIdx);
                        var getMoveClone = getMove.clone();
                        getMove.remove();
                        albumSlideList.prepend(getMoveClone);
                    }
                    
  //텍스트 슬라이드 이동
        mainAlbumSlide.goToSlide(getNext.data("index"));
        
        if(ie9 != true) {
            getActive.one("webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend", function() {
                getActive.addClass("disable");
                getActive[0].offsetHeight;
                getActive.removeClass("active zoom prev");
                getActive[0].offsetHeight;
                getActive.removeClass("disable");
            });
        }
        getActive.addClass("prev");
        
        getMoveClone.each(function(i) {
            if(getMoveIdx > 0) {
                $(this).css("left", ($(".main_album .album_slide .slide_list .btn_link").length + i) * albumMargin + albumMarginRight);
            }
            else {
                $(this).css("left", (i + getMoveIdx) * albumMargin);
            }
        });
        
        setTimeout(function() {
            $(".main_album .album_slide .slide_list .btn_link").each(function(i) {
                var getKey = i;
                var getAlbumLeft = getKey * albumMargin;
                if(getKey==6) getAlbumLeft += albumMarginLeft;
                else if(getKey>6) getAlbumLeft += albumMarginRight;
                
                if(getKey==4 || getKey==5 || getKey==6) {
                    $(this).stop(true,true).delay(80).animate({ left:getAlbumLeft }, 400, "easeInOutQuad", function() {
                        if(getKey == 6) {
                            if(ie9 == true) {
                                getActive.removeClass("active zoom prev");
                            }
                            $(this).addClass("active zoom");
                            albumCheck = true;
                        }
                    });
                }
                else {
                    $(this).stop(true,true).delay(0).animate({ left:getAlbumLeft }, 500, "easeInOutQuad");
                }
            });
        }, 300);
    }
    return false;
});
}, 10);
})
