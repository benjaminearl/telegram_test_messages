// AUDIO PLAYER
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".audio").forEach(wrapper => {
    const audio = wrapper.querySelector("audio");
    const playBtn = wrapper.querySelector(".audio__playBtn");

    playBtn.addEventListener("click", () => {
      if (audio.paused) {
        audio.play();
        playBtn.textContent = "Tune out";
      } else {
        audio.pause();
        playBtn.textContent = "Tune in";
      }
    });

    audio.addEventListener("ended", () => {
      playBtn.textContent = "Tune in";
    });
  });
});
