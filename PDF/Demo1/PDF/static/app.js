// Small UI helpers: drag-and-drop and toast
document.addEventListener('DOMContentLoaded', function(){
  document.querySelectorAll('.card input[type=file]').forEach(function(inp){
    const card = inp.closest('.card')
    card.addEventListener('dragover', e=>{e.preventDefault();card.style.transform='scale(1.01)'} )
    card.addEventListener('dragleave', e=>{card.style.transform=''})
    card.addEventListener('drop', e=>{e.preventDefault(); inp.files = e.dataTransfer.files; card.style.transform='';})
  })

  // Simple toast hide
  setTimeout(()=>{
    const t = document.querySelector('.toast')
    if(t) t.style.display='none'
  }, 4000)
})
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
let width = canvas.width = window.innerWidth;
let height = canvas.height = window.innerHeight;

const particles = [];
const particleCount = 100;

for(let i=0;i<particleCount;i++){
    particles.push({
        x: Math.random()*width,
        y: Math.random()*height,
        r: Math.random()*2 + 1,
        dx: (Math.random()-0.5)*0.5,
        dy: (Math.random()-0.5)*0.5,
        color: `rgba(0,255,255,${Math.random()*0.7+0.3})`
    });
}

function animate(){
    ctx.clearRect(0,0,width,height);
    particles.forEach(p=>{
        ctx.beginPath();
        ctx.arc(p.x,p.y,p.r,0,Math.PI*2,false);
        ctx.fillStyle = p.color;
        ctx.shadowBlur = 8;
        ctx.shadowColor = "#0ff";
        ctx.fill();
        p.x += p.dx;
        p.y += p.dy;

        if(p.x>width || p.x<0) p.dx*=-1;
        if(p.y>height || p.y<0) p.dy*=-1;
    });
    requestAnimationFrame(animate);
}
animate();

window.addEventListener('resize', ()=>{
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
});
