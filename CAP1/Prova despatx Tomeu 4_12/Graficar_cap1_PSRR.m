%root='C:\Users\Vicenç Salas\Desktop\CAP1\Prova despatx 4_12';
%% Prova deixant el gateway al despatx de'n Tomeu 300 msgs 10min
%  comparació del nombre de missatje rebut i enviat

filename = 'Datos 4_12';
sheet = 1;

dadesNRed = xlsread(filename,1);
dadesLoPy = xlsread(filename,2);
counterNR=dadesNRed(:,1);
counterLoPy=dadesLoPy(:,3);
%%
PSRR=length(counterNR)/length(counterLoPy)*100; % PSRR=97%
aux=[1];
j=2; 
k=1;
for (i=2:1:length(counterLoPy)-1)
    if j<length(counterNR)
        cNR=counterNR(j);
    else
        cNR=0;
    end
    if cNR/counterLoPy(i)==1
        aux=[aux 1];
        j=j+1;
    else
        aux =[aux 0];
    end
    
end
figure();
plot(1:1:length(counterLoPy)-1,aux);
ylim([-0.5,1.5]);
title('Missatges rebuts/perduts. Despatx Tomeu. PSRR=97%');
xlabel('Nombre de missatge');
ylabel('Rebut = 1, Perdut = 0');





