navigator.getUserMedia  = navigator.getUserMedia    || navigator.webkitGetUserMedia ||
                           navigator.mozGetUserMedia || navigator.msGetUserMedia;
var localStream = null;
var videoBlob = null;
var recorder = null;
var xhr = null;
$(".begin").click(function(){
	videoBlob = null;
	recorder = null;
	xhr = null;	
	$(".begin").addClass("hidden");
	$(".wait").removeClass("hidden");
	startVideo();
	
})


//请求媒体数据
function startVideo() {
	if(localStream){
		startRecording();
		return;
	}
    navigator.getUserMedia({video: true}, function(stream){
		localStream  = stream;
		startRecording();
	}, function(e){
		console.log('媒体错误', e);
	});
}
function startRecording() {
    if (!localStream) {
        console.warn("没有视频流");
        return;
    }
	
	console.log(3,recorder==null);
    if (recorder) {
        console.warn("录像过程已开始");
        return;
    } 
    recorder = new MediaRecorder(localStream);
    recorder.ondataavailable = function(evt) {
        console.log("数据可用，开始播放");
        videoBlob = new Blob([evt.data], { type: evt.data.type });
    }
    recorder.start();
    console.log("开始录像");
	setTimeout(function(){
			console.log("录像结束");
			recorder.stop();
			//要给一点recorder到videoBlob的时间
			setTimeout(function(){
				console.log("录像上传");
				upload_vedio();
			},1000);
		},10000);
	
	
}
function upload_vedio() {
	var fd = new FormData();
	fd.append("video", videoBlob); 
	xhr = new XMLHttpRequest(); 
	xhr.onreadystatechange = xhr_back_fun; 
	xhr.open("POST", "/upload_measure", true); 
	xhr.send(fd);
}

function xhr_back_fun(){
	if(xhr.readyState == 4 && xhr.status == 200){
		j = JSON.parse(xhr.responseText);
		if(j.is_success=="1"){
			$("#blood_glucose").val(j.blood_glucose);
			$("#blood_oxygen").val(j.blood_oxygen);
			$("#blood_pressure").val(j.blood_pressure);
			$("#body_temperature").val(j.body_temperature);
			$("#heart_rate").val(j.heart_rate);
			$("#r_id").val(j.r_id);
			$(".feature-pic").removeClass("hidden").attr("src",j.result_image)
		}
		
		//收尾动作
		$(".wait").addClass("hidden");
		$(".begin").removeClass("hidden");
	}
}

$(".motify-btn").click(function(){
	if($("#r_id").val()==null)
		return;
	$.ajax({
			cache: true,
			type: "POST",
			url:"/post_reference",
			data:$('#i-modify').serialize(),// 你的formid
			async: false,
			error: function(request) {
				alert("Connection error");
			},
			success: function(data) {
				$(".motify-btn").removeClass("hint").addClass("hint-out");
				setTimeout(function(){
					$(".motify-btn").removeClass("hint-out").addClass("hint");
				},5000);
			}
		});
})