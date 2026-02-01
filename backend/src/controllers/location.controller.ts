import { Request, Response } from "express";

const statesAndDistricts: Record<string, string[]> = {
  'Andhra Pradesh': ['Visakhapatnam', 'Vijayawada', 'Guntur', 'Krishna', 'Tirupati'],
  'Arunachal Pradesh': ['Papum Pare', 'Changlang', 'Lohit'],
  'Assam': ['Kamrup', 'Barpeta', 'Nagaon', 'Sonitpur', 'Cachar'],
  'Bihar': ['Patna', 'Gaya', 'Bhagalpur', 'Madhubani', 'Muzaffarpur'],
  'Chhattisgarh': ['Raipur', 'Bilaspur', 'Rajnandgaon', 'Durg', 'Bastar'],
  'Delhi': ['Central', 'East', 'West', 'North', 'South'],
  'Goa': ['North Goa', 'South Goa'],
  'Gujarat': ['Ahmedabad', 'Vadodara', 'Surat', 'Rajkot', 'Jamnagar'],
  'Haryana': ['Faridabad', 'Gurgaon', 'Hisar', 'Rohtak', 'Panipat'],
  'Himachal Pradesh': ['Shimla', 'Mandi', 'Kangra', 'Solan'],
  'Jharkhand': ['Ranchi', 'Dhanbad', 'Giridih', 'Hazaribagh'],
  'Karnataka': ['Bengaluru', 'Mysore', 'Mangalore', 'Belgaum'],
  'Kerala': ['Thiruvananthapuram', 'Kochi', 'Kozhikode', 'Kottayam'],
  'Madhya Pradesh': ['Indore', 'Bhopal', 'Jabalpur', 'Gwalior'],
  'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Aurangabad', 'Nashik'],
  'Manipur': ['Imphal', 'Churachandpur', 'Bishnupur'],
  'Meghalaya': ['Shillong', 'Khasi Hills', 'Garo Hills', 'Jaintia Hills'],
  'Mizoram': ['Aizawl', 'Lunglei', 'Champhai'],
  'Nagaland': ['Kohima', 'Dimapur', 'Mokokchung'],
  'Odisha': ['Bhubaneswar', 'Cuttack', 'Rourkela', 'Sambalpur'],
  'Punjab': ['Amritsar', 'Ludhiana', 'Jalandhar', 'Patiala'],
  'Rajasthan': ['Jaipur', 'Jodhpur', 'Udaipur', 'Ajmer'],
  'Sikkim': ['Gangtok', 'East Sikkim', 'West Sikkim'],
  'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Salem'],
  'Telangana': ['Hyderabad', 'Warangal', 'Karimnagar', 'Nizamabad'],
  'Tripura': ['Agartala', 'West Tripura', 'Sipahijala'],
  'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Varanasi', 'Agra', 'Allahabad'],
  'Uttarakhand': ['Dehradun', 'Haridwar', 'Nainital', 'Almora'],
  'West Bengal': ['Kolkata', 'Howrah', 'Darjeeling', 'Jalpaiguri'],
};

export const getStates = (req: Request, res: Response) => {
  try {
    const states = Object.keys(statesAndDistricts).sort();
    res.json({
      success: true,
      message: "States retrieved successfully",
      data: states,
    });
  } catch (error: any) {
    res.status(500).json({ success: false, message: error.message });
  }
};

export const getDistricts = (req: Request, res: Response) => {
  try {
    const { state } = req.params;
    if (!state) return res.status(400).json({ success: false, message: "State parameter required" });
    const districts = statesAndDistricts[state] || [];
    if (!districts.length) return res.status(404).json({ success: false, message: `No districts found for ${state}` });
    res.json({ success: true, message: "Districts retrieved", data: districts });
  } catch (error: any) {
    res.status(500).json({ success: false, message: error.message });
  }
};
