import { FilterQuery } from "mongoose";
import Judgment from "../models/judgment.model";

interface QueryParams {
  page?: string;
  limit?: string;
  category?: string;
  year?: string;
  courtType?: string;
  courtCode?: string;
  confidenceMin?: string;
  search?: string;
  sortBy?: string;
  sortOrder?: string;
}

export const buildJudgmentQuery = (query: QueryParams) => {
  const filter: FilterQuery<typeof Judgment> = {};

  // Filtering
  if (query.category) {
    filter.category = query.category;
  }

  if (query.year) {
    filter.year = query.year;
  }

  if (query.courtType) {
    filter.courtType = query.courtType;
  }

  if (query.courtCode) {
    filter.courtCode = query.courtCode;
  }

  if (query.confidenceMin) {
    filter.confidence = { $gte: parseFloat(query.confidenceMin) };
  }

  if (query.search) {
    filter.$text = { $search: query.search };
  }

  // Pagination
  const page = Math.max(parseInt(query.page || "1"), 1);
  const limit = Math.min(parseInt(query.limit || "20"), 100);
  const skip = (page - 1) * limit;

  // Sorting
  const sortField = query.sortBy || "createdAt";
  const sortOrder = query.sortOrder === "asc" ? 1 : -1;

  const sort: any = {};

  if (query.search) {
    sort.score = { $meta: "textScore" };
  } else {
    sort[sortField] = sortOrder;
  }

  return {
    filter,
    page,
    limit,
    skip,
    sort,
  };
};
