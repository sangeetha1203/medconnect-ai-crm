import { createSlice } from "@reduxjs/toolkit";

const interactionSlice = createSlice({
  name: "interaction",
  initialState: {
    data: [],
    searchResults: [],
    analytics: {
      totalInteractions: 0,
      highPriority: 0,
      avgScore: 88,
    },
  },
  reducers: {
    setInteractions: (state, action) => {
      state.data = action.payload;
      state.analytics.totalInteractions = action.payload.length;
    },

    setSearchResults: (state, action) => {
      state.searchResults = action.payload;
    },

    setAnalytics: (state, action) => {
      state.analytics = action.payload;
    },
  },
});

export const {
  setInteractions,
  setSearchResults,
  setAnalytics,
} = interactionSlice.actions;

export default interactionSlice.reducer;