const imagemin = require('imagemin');
const imageminJpegtran = require('imagemin-jpegtran');
const imageminPngquant = require('imagemin-pngquant');
const path = require('path');

(async () => {
  const imagesDir = path.join(__dirname, 'src/assets/images');
  
  await imagemin([`${imagesDir}/**/*.{jpg,jpeg,png,svg}`], {
    destination: imagesDir,
    plugins: [
      imageminJpegtran(),
      imageminPngquant({
        quality: [0.6, 0.8]
      })
    ]
  });
  
  console.log('✓ Images optimized!');
})();