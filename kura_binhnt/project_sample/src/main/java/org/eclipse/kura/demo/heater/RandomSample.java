package org.eclipse.kura.demo.heater;


import java.math.BigInteger;
import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Created by nguyenbinh on 18/08/2016.
 */
public class RandomSample {

    public static SmartRoom smartRoom = null;

    public ArrayList<String> getRandom(ConfigUtils.ConfigObject configObject){
        setSmartRoom(configObject);
        return smartRoom.getStatus();
    }


    private void setSmartRoom(ConfigUtils.ConfigObject configObject){
        if(smartRoom == null){
            smartRoom = new SmartRoom();
            smartRoom.setIdPhong(configObject.getIdPhong()+"_"+new BigInteger(130, new SecureRandom()).toString(32));
            smartRoom.setSoCumSensor(configObject.getSoCumSensor());
            smartRoom.setSoKhuVuc(configObject.getSoKhuVuc());
            List<DuLieu> duLieus = new ArrayList<DuLieu>();
            smartRoom.setDuLieu(duLieus);
            for (int i = 0; i < smartRoom.getSoKhuVuc(); i++){
                DuLieu temp = new DuLieu();
                temp.setIdKv(configObject.getDuLieu().get(i).getId());
                temp.setRandomConfig(configObject.getDuLieu().get(i).getDanhSach());
                List<DanhSach> danhSachCumSensor = new ArrayList<DanhSach>();
                int soCum = smartRoom.getSoCumSensor() / smartRoom.getSoKhuVuc();
                if(i == smartRoom.getSoKhuVuc() - 1) soCum = soCum + smartRoom.getSoCumSensor() - (smartRoom.getSoCumSensor() / smartRoom.getSoKhuVuc())*smartRoom.getSoKhuVuc();
                temp.setSoCumSensor(soCum);
                for(int j = 0; j < soCum; j++){
                    DanhSach tempCum = new DanhSach();
                    tempCum.setIdCum(configObject.getDuLieu().get(i).getId()+"_"+(j+1));
                    danhSachCumSensor.add(tempCum);
                }
                temp.setDanhSach(danhSachCumSensor);
                duLieus.add(temp);
            }
        }
    }

    public class DanhSach {

        private String idCum;
        
        private Integer nhietDo;
        
        private Integer doAm;
        
        private Integer soNguoi;


        /**
         *
         * @return
         * The idCum
         */
        public String getIdCum() {
            return idCum;
        }

        /**
         *
         * @param idCum
         * The id_cum
         */
        public void setIdCum(String idCum) {
            this.idCum = idCum;
        }

        /**
         *
         * @return
         * The nhietDo
         */
        public Integer getNhietDo() {
            return nhietDo;
        }

        /**
         *
         * @param nhietDo
         * The nhiet_do
         */
        public void setNhietDo(Integer nhietDo) {
            this.nhietDo = nhietDo;
        }

        /**
         *
         * @return
         * The doAm
         */
        public Integer getDoAm() {
            return doAm;
        }

        /**
         *
         * @param doAm
         * The do_am
         */
        public void setDoAm(Integer doAm) {
            this.doAm = doAm;
        }

        /**
         *
         * @return
         * The soNguoi
         */
        public Integer getSoNguoi() {
            return soNguoi;
        }

        /**
         *
         * @param soNguoi
         * The so_nguoi
         */
        public void setSoNguoi(Integer soNguoi) {
            this.soNguoi = soNguoi;
        }
    }

    public class DuLieu {

        
        private String idKv;
        
        private Integer soCumSensor;
        
        private List<DanhSach> danhSach = new ArrayList<DanhSach>();
        private List<ConfigUtils.DanhSach> randomConfig;


        /**
         *
         * @return
         * The idKv
         */
        public String getIdKv() {
            return idKv;
        }

        /**
         *
         * @param idKv
         * The id_kv
         */
        public void setIdKv(String idKv) {
            this.idKv = idKv;
        }

        /**
         *
         * @return
         * The soCumSensor
         */
        public Integer getSoCumSensor() {
            return soCumSensor;
        }

        /**
         *
         * @param soCumSensor
         * The so_cum_sensor
         */
        public void setSoCumSensor(Integer soCumSensor) {
            this.soCumSensor = soCumSensor;
        }

        /**
         *
         * @return
         * The danhSach
         */
        public List<DanhSach> getDanhSach() {
            return danhSach;
        }

        /**
         *
         * @param danhSach
         * The danh_sach
         */
        public void setDanhSach(List<DanhSach> danhSach) {
            this.danhSach = danhSach;
        }

        public List<ConfigUtils.DanhSach> getRandomConfig() {
            return randomConfig;
        }

        public void setRandomConfig(List<ConfigUtils.DanhSach> randomConfig) {
            this.randomConfig = randomConfig;
        }
    }

    public class SmartRoom {

       
        private String idPhong;
        private Integer soCumSensor;
        private Integer soKhuVuc;
        private List<DuLieu> duLieu = new ArrayList<DuLieu>();
        private Random random = new Random();
        /**
         *
         * @return
         * The idPhong
         */
        public String getIdPhong() {
            return idPhong;
        }

        /**
         *
         * @param idPhong
         * The id_phong
         */
        public void setIdPhong(String idPhong) {
            this.idPhong = idPhong;
        }

        /**
         *
         * @return
         * The soCumSensor
         */
        public Integer getSoCumSensor() {
            return soCumSensor;
        }

        /**
         *
         * @param soCumSensor
         * The so_cum_sensor
         */
        public void setSoCumSensor(Integer soCumSensor) {
            this.soCumSensor = soCumSensor;
        }

        /**
         *
         * @return
         * The soKhuVuc
         */
        public Integer getSoKhuVuc() {
            return soKhuVuc;
        }

        /**
         *
         * @param soKhuVuc
         * The so_khu_vuc
         */
        public void setSoKhuVuc(Integer soKhuVuc) {
            this.soKhuVuc = soKhuVuc;
        }

        /**
         *
         * @return
         * The duLieu
         */
        public List<DuLieu> getDuLieu() {
            return duLieu;
        }

        /**
         *
         * @param duLieu
         * The du_lieu
         */
        public void setDuLieu(List<DuLieu> duLieu) {
            this.duLieu = duLieu;
        }

        public ArrayList<String> getStatus(){
            ArrayList<String> status = new ArrayList<String>();
            for(int i = 0; i < soKhuVuc; i++){
                DuLieu khuVuc = duLieu.get(i);
                for(int j = 0; j < khuVuc.getSoCumSensor(); j++){
                    DanhSach cum = khuVuc.getDanhSach().get(j);
                    for(int k = 0; k < khuVuc.getRandomConfig().size(); k++){
                        if(khuVuc.getRandomConfig().get(k).getTag().equals("sensor_nhiet_do")){
                            cum.setNhietDo(random.nextInt(khuVuc.getRandomConfig().get(k).getMax() - khuVuc.getRandomConfig().get(k).getMin()) + khuVuc.getRandomConfig().get(k).getMin());
                        } else if(khuVuc.getRandomConfig().get(k).getTag().equals("sensor_do_am")){
                            cum.setDoAm(random.nextInt(khuVuc.getRandomConfig().get(k).getMax() - khuVuc.getRandomConfig().get(k).getMin()) + khuVuc.getRandomConfig().get(k).getMin());
                        }else if(khuVuc.getRandomConfig().get(k).getTag().equals("sensor_dem_nguoi")){
                            cum.setSoNguoi(random.nextInt(khuVuc.getRandomConfig().get(k).getMax() - khuVuc.getRandomConfig().get(k).getMin()) + khuVuc.getRandomConfig().get(k).getMin());
                        }
                    }
                    String temp = "idp " + idPhong + " idkv " + khuVuc.getIdKv() + " idcum " + cum.getIdCum() + " nhietdo " + cum.getNhietDo() + " doam " + cum.getDoAm() + " nguoi " + cum.getSoNguoi();
                    status.add(temp);
                }
            }
            return status;
        }
    }

}
