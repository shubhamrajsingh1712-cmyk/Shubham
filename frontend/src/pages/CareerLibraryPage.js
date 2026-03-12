import { useState, useEffect, useCallback } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { TrendingUp, Search, ChevronRight, ArrowLeft, Briefcase, X } from 'lucide-react';
import axios from 'axios';

const API_URL = `${process.env.REACT_APP_BACKEND_URL}/api`;

const ICON_COLORS = {
  eng: "#3B82F6", med: "#10B981", biz: "#8B5CF6", art: "#EC4899",
  sci: "#06B6D4", law: "#F59E0B", edu: "#6366F1", gov: "#EF4444",
  media: "#F97316", agri: "#22C55E", hosp: "#0EA5E9", def: "#64748B",
  sport: "#A855F7", social: "#14B8A6",
};

const GROWTH_BADGES = {
  Excellent: "bg-green-100 text-green-700",
  Good: "bg-blue-100 text-blue-700",
  Moderate: "bg-yellow-100 text-yellow-700",
  Emerging: "bg-purple-100 text-purple-700",
};

export default function CareerLibraryPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [categories, setCategories] = useState([]);
  const [careers, setCareers] = useState([]);
  const [total, setTotal] = useState(0);
  const [pages, setPages] = useState(1);
  const [loading, setLoading] = useState(true);

  const activeCategory = searchParams.get('category') || '';
  const searchQuery = searchParams.get('q') || '';
  const currentPage = parseInt(searchParams.get('page') || '1', 10);

  useEffect(() => {
    axios.get(`${API_URL}/careers/categories`).then(res => setCategories(res.data)).catch(() => {});
  }, []);

  const fetchCareers = useCallback(async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/careers/search`, {
        params: { q: searchQuery, category: activeCategory, page: currentPage, limit: 24 },
      });
      setCareers(res.data.careers);
      setTotal(res.data.total);
      setPages(res.data.pages);
    } catch {
      setCareers([]);
    } finally {
      setLoading(false);
    }
  }, [searchQuery, activeCategory, currentPage]);

  useEffect(() => { fetchCareers(); }, [fetchCareers]);

  const updateParams = (updates) => {
    const params = new URLSearchParams(searchParams);
    Object.entries(updates).forEach(([k, v]) => {
      if (v) params.set(k, v);
      else params.delete(k);
    });
    if (updates.category !== undefined || updates.q !== undefined) params.delete('page');
    setSearchParams(params);
  };

  const activeCatData = categories.find(c => c.id === activeCategory);

  return (
    <div className="min-h-screen bg-background">
      {/* Nav */}
      <nav className="bg-white border-b border-black/5 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
                <TrendingUp className="text-white" size={24} />
              </div>
              <span className="text-xl font-heading font-bold text-primary">BoatMyCareer</span>
            </Link>
            <div className="flex items-center space-x-4">
              <Link to="/">
                <Button variant="ghost" size="sm" data-testid="back-home-btn">
                  <ArrowLeft size={16} className="mr-1" /> Home
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="bg-primary text-white py-12 md:py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl sm:text-5xl font-heading font-bold mb-3" data-testid="career-library-title">
            Career Library
          </h1>
          <p className="text-lg opacity-90 mb-6 max-w-2xl">
            Explore {total || '300'}+ career paths across {categories.length} domains. Find detailed info on education, skills, salaries & growth.
          </p>
          <div className="relative max-w-xl">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
            <Input
              data-testid="career-search-input"
              placeholder="Search careers by name or skill..."
              className="pl-10 py-6 text-base bg-white text-gray-900 border-0 rounded-xl"
              value={searchQuery}
              onChange={e => updateParams({ q: e.target.value })}
            />
            {searchQuery && (
              <button onClick={() => updateParams({ q: '' })} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                <X size={18} />
              </button>
            )}
          </div>
        </div>
      </section>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar */}
          <aside className="lg:w-64 flex-shrink-0">
            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">Categories</h3>
            <div className="space-y-1">
              <button
                data-testid="category-all"
                onClick={() => updateParams({ category: '' })}
                className={`w-full text-left px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${!activeCategory ? 'bg-primary text-white' : 'text-gray-700 hover:bg-gray-100'}`}
              >
                All Careers
                <span className="float-right opacity-70">{categories.reduce((a, c) => a + c.count, 0)}</span>
              </button>
              {categories.map(cat => (
                <button
                  key={cat.id}
                  data-testid={`category-${cat.id}`}
                  onClick={() => updateParams({ category: cat.id })}
                  className={`w-full text-left px-3 py-2.5 rounded-lg text-sm font-medium transition-colors flex items-center justify-between ${activeCategory === cat.id ? 'bg-primary text-white' : 'text-gray-700 hover:bg-gray-100'}`}
                >
                  <span className="flex items-center gap-2">
                    <span className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ backgroundColor: ICON_COLORS[cat.id] }}></span>
                    <span className="truncate">{cat.name}</span>
                  </span>
                  <span className="opacity-70 ml-1">{cat.count}</span>
                </button>
              ))}
            </div>
          </aside>

          {/* Main */}
          <main className="flex-1 min-w-0">
            {/* Active filters */}
            <div className="flex items-center justify-between mb-6 flex-wrap gap-2">
              <div className="flex items-center gap-2 flex-wrap">
                {activeCatData && (
                  <span className="inline-flex items-center gap-1 bg-primary/10 text-primary text-sm font-medium px-3 py-1 rounded-full">
                    {activeCatData.name}
                    <button onClick={() => updateParams({ category: '' })} className="ml-1 hover:text-primary/70"><X size={14} /></button>
                  </span>
                )}
                {searchQuery && (
                  <span className="inline-flex items-center gap-1 bg-accent/10 text-accent text-sm font-medium px-3 py-1 rounded-full">
                    "{searchQuery}"
                    <button onClick={() => updateParams({ q: '' })} className="ml-1 hover:text-accent/70"><X size={14} /></button>
                  </span>
                )}
              </div>
              <span className="text-sm text-gray-500" data-testid="career-count">{total} careers found</span>
            </div>

            {loading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="h-48 bg-gray-100 rounded-xl animate-pulse" />
                ))}
              </div>
            ) : careers.length === 0 ? (
              <div className="text-center py-16">
                <Briefcase className="mx-auto text-gray-300 mb-4" size={48} />
                <h3 className="text-lg font-semibold text-gray-600 mb-2">No careers found</h3>
                <p className="text-gray-500 mb-4">Try adjusting your search or filter</p>
                <Button variant="outline" onClick={() => { updateParams({ q: '', category: '' }); }}>Clear Filters</Button>
              </div>
            ) : (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                  {careers.map(career => (
                    <Link key={career.slug} to={`/careers/${career.slug}`} data-testid={`career-card-${career.slug}`}>
                      <Card className="card-base h-full p-5 hover:-translate-y-1 hover:shadow-float transition-all duration-300 cursor-pointer group">
                        <div className="flex items-start justify-between mb-3">
                          <div className="flex-1 min-w-0">
                            <h3 className="font-heading font-semibold text-primary group-hover:text-accent transition-colors truncate">
                              {career.name}
                            </h3>
                            <p className="text-xs text-gray-500 mt-0.5">{career.stream}</p>
                          </div>
                          <span className={`text-xs font-semibold px-2 py-0.5 rounded-full flex-shrink-0 ml-2 ${GROWTH_BADGES[career.growth_outlook] || GROWTH_BADGES.Good}`}>
                            {career.growth_outlook}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 line-clamp-2 mb-3">{career.description}</p>
                        <div className="flex flex-wrap gap-1 mb-3">
                          {career.skills_required.slice(0, 3).map(skill => (
                            <span key={skill} className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded">{skill}</span>
                          ))}
                        </div>
                        <div className="flex items-center justify-between text-xs text-gray-500 pt-2 border-t border-gray-100">
                          <span>{career.salary?.starting || 'Varies'}</span>
                          <span className="flex items-center text-primary font-medium group-hover:text-accent transition-colors">
                            View Details <ChevronRight size={14} />
                          </span>
                        </div>
                      </Card>
                    </Link>
                  ))}
                </div>

                {/* Pagination */}
                {pages > 1 && (
                  <div className="flex justify-center items-center gap-2 mt-8">
                    <Button
                      variant="outline" size="sm"
                      disabled={currentPage <= 1}
                      onClick={() => updateParams({ page: String(currentPage - 1) })}
                      data-testid="pagination-prev"
                    >
                      Previous
                    </Button>
                    <span className="text-sm text-gray-600 px-3">
                      Page {currentPage} of {pages}
                    </span>
                    <Button
                      variant="outline" size="sm"
                      disabled={currentPage >= pages}
                      onClick={() => updateParams({ page: String(currentPage + 1) })}
                      data-testid="pagination-next"
                    >
                      Next
                    </Button>
                  </div>
                )}
              </>
            )}
          </main>
        </div>
      </div>
    </div>
  );
}
