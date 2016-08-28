package org.eclipse.kura.demo.heater;
import com.google.gson.Gson;
import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;
import com.google.gson.internal.LinkedTreeMap;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import javax.annotation.Generated;

/**        s_logger.info(dataConfig);
 * Created by nguyenbinh on 17/08/2016.
 */
public class ConfigUtils {

    public ConfigObject getConfigObject(String filePath){
        String dataConfig = "";
        try {
            BufferedReader br = new BufferedReader(new FileReader(filePath));
            StringBuilder sb = new StringBuilder();
            String line = br.readLine();

            while (line != null) {
                sb.append(line);
                sb.append(System.lineSeparator());
                line = br.readLine();
            }
            dataConfig = sb.toString();
            br.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
        Heater.s_logger.info("Create json");
        Gson gson = new Gson();
        LinkedTreeMap object = (LinkedTreeMap) gson.fromJson(dataConfig, Object.class);

        ConfigObject configObject = new ConfigObject();
        configObject.setIdPhong((String)object.get("id_phong"));
        configObject.setSoKhuVuc(((Double)object.get("so_khu_vuc")).intValue());
        configObject.setSoCumSensor(((Double)object.get("so_cum_sensor")).intValue());
        List<DuLieu> duLieus = new ArrayList<DuLieu>();
        ArrayList<LinkedTreeMap> listConfigKhuVuc = (ArrayList<LinkedTreeMap>) object.get("du_lieu");
        for(int i = 0 ; i < configObject.getSoKhuVuc(); i++){
            LinkedTreeMap data = listConfigKhuVuc.get(i);
            DuLieu configKhuVuc = new DuLieu();
            configKhuVuc.setId((String)data.get("id"));
            configKhuVuc.setSoLoaiSensor(((Double)data.get("so_loai_sensor")).intValue());

            List<DanhSach> danhSachLoaiSensor = new ArrayList<DanhSach>();
            ArrayList<LinkedTreeMap> dataSensor = (ArrayList<LinkedTreeMap>) data.get("danh_sach");
            for(int j = 0; j < configKhuVuc.getSoLoaiSensor(); j++){
                DanhSach temp = new DanhSach();
                LinkedTreeMap tempsensor = dataSensor.get(j);
                temp.setTag((String)tempsensor.get("tag"));
                temp.setMax(((Double)tempsensor.get("max")).intValue());
                temp.setMin(((Double)tempsensor.get("min")).intValue());
                danhSachLoaiSensor.add(temp);
            }
            configKhuVuc.setDanhSach(danhSachLoaiSensor);
            duLieus.add(configKhuVuc);
        }
        configObject.setDuLieu(duLieus);
        Heater.s_logger.info("Create json ok");
        return configObject;
    }

    @Generated("org.jsonschema2pojo")
    public class ConfigObject {

    @SerializedName("id_phong")
    @Expose
    private String idPhong;
    @SerializedName("so_cum_sensor")
    @Expose
    private Integer soCumSensor;
    @SerializedName("so_khu_vuc")
    @Expose
    private Integer soKhuVuc;
    @SerializedName("du_lieu")
    @Expose
    private List<DuLieu> duLieu = new ArrayList<DuLieu>();

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

    }

    @Generated("org.jsonschema2pojo")
    public class DanhSach {

    @SerializedName("tag")
    @Expose
    private String tag;
    @SerializedName("min")
    @Expose
    private Integer min;
    @SerializedName("max")
    @Expose
    private Integer max;

    /**
    * 
    * @return
    * The tag
    */
    public String getTag() {
    return tag;
    }

    /**
    * 
    * @param tag
    * The tag
    */
    public void setTag(String tag) {
    this.tag = tag;
    }

    /**
    * 
    * @return
    * The min
    */
    public Integer getMin() {
    return min;
    }

    /**
    * 
    * @param min
    * The min
    */
    public void setMin(Integer min) {
    this.min = min;
    }

    /**
    * 
    * @return
    * The max
    */
    public Integer getMax() {
    return max;
    }

    /**
    * 
    * @param max
    * The max
    */
    public void setMax(Integer max) {
    this.max = max;
    }

    }
    
    @Generated("org.jsonschema2pojo")
    public class DuLieu {

    @SerializedName("id")
    @Expose
    private String id;
    @SerializedName("so_loai_sensor")
    @Expose
    private Integer soLoaiSensor;
    @SerializedName("danh_sach")
    @Expose
    private List<DanhSach> danhSach = new ArrayList<DanhSach>();

    /**
    * 
    * @return
    * The id
    */
    public String getId() {
    return id;
    }

    /**
    * 
    * @param id
    * The id
    */
    public void setId(String id) {
    this.id = id;
    }

    /**
    * 
    * @return
    * The soLoaiSensor
    */
    public Integer getSoLoaiSensor() {
    return soLoaiSensor;
    }

    /**
    * 
    * @param soLoaiSensor
    * The so_loai_sensor
    */
    public void setSoLoaiSensor(Integer soLoaiSensor) {
    this.soLoaiSensor = soLoaiSensor;
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

    }
}
