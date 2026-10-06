package com.campusfind.model;
public class Item {
    private int id;
    private int userId;
    private String itemName;
    private String category;
    private String type;
    private String location;
    private String dateReported;
    private String description;
    private String status;
    
    public Item() {}
    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public int getUserId() { return userId; }
    public void setUserId(int userId) { this.userId = userId; }
    public String getItemName() { return itemName; }
    public void setItemName(String itemName) { this.itemName = itemName; }
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
    public String getLocation() { return location; }
    public void setLocation(String location) { this.location = location; }
    public String getDateReported() { return dateReported; }
    public void setDateReported(String dateReported) { this.dateReported = dateReported; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
}
