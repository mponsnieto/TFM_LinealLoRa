filename = 'Datos_BBQ.xlsx';

dadesBMP = importfile1(filename,'datos_bmp');
time_bmp=dadesBMP.Column2(1:98);
temp_bmp=dadesBMP.Column3(1:98);

dadesCAM = importfile1(filename,'datos_cam');
time_cam=dadesCAM.Column2(1:98);
temp_cam=dadesCAM.Column3(1:98);

dadesHTU = importfile1(filename,'datos_htu');
time_htu=dadesHTU.Column2(1:98);
temp_htu=dadesHTU.Column3(1:98);

dadesMCP = importfile1(filename,'datos_mcp');
time_mcp=dadesMCP.Column2(41:end);
temp_mcp=dadesMCP.Column3(41:end);

dadesQAire = importfile2(filename,'datos_QAire');
time_QAire=dadesQAire.Column2(17:end);
pm1=dadesQAire.Column3(17:end);
pm25=dadesQAire.Column4(17:end);
pm10=dadesQAire.Column5(17:end);
%% Graficar temperaturas
figure();plot(time_bmp,temp_bmp);
hold on
plot(time_cam,temp_cam);
plot(time_htu,temp_htu);
plot(time_mcp,temp_mcp);
temp_amb=temp_bmp;
temp_amb(:)=26.0;
plot(time_bmp,temp_amb);
title('Evolució de la temperatura');
ylabel('Temp [ºC]');
xlabel('Relative time [hh:mm:ss]');
legend('BMP','CAM','HTU','MCP','AMB');
hold off
%% Grafic qualitat aire
figure(); hold on;plot(time_QAire,pm1,'-x');
plot(time_QAire,pm25,'-x');
plot(time_QAire,pm10,'-x');
title('Evolució de les particules en suspensió');
ylabel('Particules [ug/m3]');
xlabel('Relative time [hh:mm:ss]');
legend('pm1','pm2.5','pm10');