import { Request, Response } from 'express';

export const getActsByCategory = async (req: Request, res: Response) => {
  const { category } = req.query;

  if (!category) {
    return res.status(400).json({
      success: false,
      message: 'Category is required',
    });
  }

  // Temporary mock data (safe, replace later with DB)
  const actsMap: Record<string, string[]> = {
    civil: [
      'Code of Civil Procedure, 1908',
      'Transfer of Property Act, 1882',
      'Specific Relief Act, 1963',
    ],
    criminal: [
      'Indian Penal Code, 1860',
      'Code of Criminal Procedure, 1973',
      'BNSS, 2023',
    ],
    service: [
      'Central Civil Services Rules',
      'Service Conduct Rules',
    ],
    tax: [
      'Income Tax Act, 1961',
      'GST Act, 2017',
    ],
  };

  return res.json({
    success: true,
    category,
    acts: actsMap[String(category)] || [],
  });
};
