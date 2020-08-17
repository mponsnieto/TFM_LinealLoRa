%root='C:\Users\Vicenç Salas\Desktop\CAP1;
%% Comparam la qualitat de senyal entre el despatx dels veins i el despatx den Tomeu

dadesEnfora_10min = xlsread('.\Prova despatx Tomeu 4_12\Datos 4_12',1);
dadesEnfora_5min = xlsread('.\Lab Tomeu 18_11\Datos 18_11',1);
dadesDinsLab = xlsread('.\Entre_Labs\Dades NodeRed capitol 1',1);
dadesAprop = xlsread('.\Entre_Labs\Dades NodeRed capitol 1',2);
%% Rssi
numMsg=dadesEnfora_10min(:,1);
rssi_enfora_10=dadesEnfora_10min(:,12);
rssi_enfora_5=dadesEnfora_5min(1:length(rssi_enfora_10),12);
rssi_aprop=dadesAprop(1:length(rssi_enfora_10),11);
rssi_dins=dadesDinsLab(1:length(rssi_enfora_10),11);
figure; plot(numMsg,rssi_dins,numMsg,rssi_aprop,numMsg,rssi_enfora_5,numMsg,rssi_enfora_10);
title('Rssi en les diferents proves');
legend('5m','7m','20m_{5min}','20m_{10min}'); ylabel('rssi [dBm]'); xlabel('numMsg');

%% SNR
numMsg=dadesEnfora_10min(:,1);
snr_enfora_10=dadesEnfora_10min(:,13);
snr_enfora_5=dadesEnfora_5min(1:length(snr_enfora_10),13);
snr_aprop=dadesAprop(1:length(snr_enfora_10),12);
snr_dins=dadesDinsLab(1:length(snr_enfora_10),12);
figure; plot(numMsg,snr_enfora_5,numMsg,snr_enfora_10,numMsg,snr_dins,numMsg,snr_aprop);
title('SNR en les diferents proves');
legend('Lab tomeu_{5min}','Lab tomeu_{10min}','5m','entre labs'); ylabel('snr'); xlabel('numMsg');
%% SNR bar

snr_enfora_10=dadesEnfora_10min(:,13);
snr_enfora_5=dadesEnfora_5min(1:length(snr_enfora_10),13);
snr_aprop=dadesAprop(1:length(snr_enfora_10),12);
snr_dins=dadesDinsLab(1:length(snr_enfora_10),12);
min_snr=min([min(snr_enfora_10) min(snr_enfora_5) min(snr_aprop) min(snr_dins)])
max_snr=max([max(snr_enfora_10) max(snr_enfora_5) max(snr_aprop) max(snr_dins)])
num_snr=[[] []]
k=1
for i=min_snr:1:max_snr
    num_snr(k,4)=length(find(snr_enfora_10==i));
    num_snr(k,3)=length(find(snr_enfora_5==i));
    num_snr(k,2)=length(find(snr_aprop==i));
    num_snr(k,1)=length(find(snr_dins==i));
    k=k+1;
end
j=min_snr:1:max_snr
figure; bar(j,num_snr);
%figure; bar(num_snr,'stacked');
title('SNR en les diferents proves');
legend('5m','7m','20m_{5min}','20m_{10min}'); ylabel('numMsg'); xlabel('SNR[dB]');