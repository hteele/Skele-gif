video = VideoReader("cat_test.mp4");
totalFrames = video.numFrames;

% Processes every x-th frame 
frameRate = 5;

folder = 'FOLDER_NAME';
outputDir = fullfile(pwd, folder);

if ~exist(outputDir, 'dir')
    mkdir(outputDir);
end

for i = 1:frameRate:totalFrames
    frames = readFrame(video);
    fileName = fullfile(outputDir, sprintf('FRAME%d.png', i));
    imwrite(frames, fileName);
end
