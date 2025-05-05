import React, { useState, useEffect, useRef } from 'react';
import Map, { Marker, Popup, MapRef } from 'react-map-gl';
import { useNavigate } from 'react-router-dom';
import { Star, MapPin, Loader2 } from 'lucide-react';
import { searchHouses } from '../api/house';
import useSupercluster from 'use-supercluster';
import 'mapbox-gl/dist/mapbox-gl.css';

// Mock data for initial map view (Moscow center)
const INITIAL_VIEW_STATE = {
  latitude: 55.7558,
  longitude: 37.6173,
  zoom: 10
};

// MapBox token would typically come from environment variables
const MAPBOX_TOKEN = "pk.eyJ1IjoiZXhhbXBsZXVzZXIiLCJhIjoiY2tleTFsODByMDA5YzJ4bnhyeG92NHhmZiJ9.example";

interface House {
  id: string;
  address: string;
  latitude: number;
  longitude: number;
  rating?: number;
  reviews_count?: number;
}

const MapPage: React.FC = () => {
  const navigate = useNavigate();
  const mapRef = useRef<MapRef>(null);
  const [houses, setHouses] = useState<House[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [viewState, setViewState] = useState(INITIAL_VIEW_STATE);
  const [selectedHouse, setSelectedHouse] = useState<House | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [bounds, setBounds] = useState<[number, number, number, number]>([0, 0, 0, 0]);

  // Fetch houses on initial load or when search changes
  useEffect(() => {
    const loadHouses = async () => {
      if (!searchQuery) return;
      
      setIsLoading(true);
      try {
        const results = await searchHouses(searchQuery);
        setHouses(results.filter((house: any) => 
          house.latitude && house.longitude
        ));
      } catch (error) {
        console.error('Error loading houses:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadHouses();
  }, [searchQuery]);

  // Update bounds when map moves
  const onMapMove = React.useCallback(() => {
    if (!mapRef.current) return;
    
    const bounds = mapRef.current.getMap().getBounds().toArray();
    setBounds([
      bounds[0][0], // westLng
      bounds[0][1], // southLat
      bounds[1][0], // eastLng
      bounds[1][1]  // northLat
    ]);
  }, []);

  // Convert houses to GeoJSON points for clustering
  const points = React.useMemo(() => {
    return houses.map(house => ({
      type: 'Feature',
      properties: { cluster: false, houseId: house.id, ...house },
      geometry: {
        type: 'Point',
        coordinates: [house.longitude, house.latitude]
      }
    }));
  }, [houses]);

  // Setup supercluster
  const { clusters, supercluster } = useSupercluster({
    points,
    bounds,
    zoom: viewState.zoom,
    options: { radius: 75, maxZoom: 20 }
  });

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    // Search is triggered by the state change above
  };

  const handleHouseClick = (house: House) => {
    setSelectedHouse(house);
  };

  const handlePopupClose = () => {
    setSelectedHouse(null);
  };

  const handleViewHouse = () => {
    if (selectedHouse) {
      navigate(`/house/${selectedHouse.id}`);
    }
  };

  return (
    <div className="h-[calc(100vh-160px)] min-h-[500px] flex flex-col">
      <div className="mb-4">
        <h1 className="text-3xl font-bold mb-2">Карта домов</h1>
        <form onSubmit={handleSearch} className="flex gap-2">
          <div className="relative flex-grow">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Поиск домов на карте..."
              className="w-full p-3 pl-10 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
          </div>
          <button
            type="submit"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
            disabled={isLoading}
          >
            {isLoading ? (
              <span className="flex items-center"><Loader2 className="animate-spin mr-2" size={18} /> Поиск</span>
            ) : (
              'Найти'
            )}
          </button>
        </form>
      </div>

      <div className="relative flex-grow border rounded-lg overflow-hidden">
        <Map
          ref={mapRef}
          mapStyle="mapbox://styles/mapbox/streets-v11"
          mapboxAccessToken={MAPBOX_TOKEN}
          {...viewState}
          onMove={evt => {
            setViewState(evt.viewState);
            onMapMove();
          }}
          onLoad={onMapMove}
        >
          {clusters.map(cluster => {
            const [longitude, latitude] = cluster.geometry.coordinates;
            const { cluster: isCluster, point_count: pointCount } = cluster.properties;

            if (isCluster) {
              return (
                <Marker
                  key={`cluster-${cluster.id}`}
                  latitude={latitude}
                  longitude={longitude}
                >
                  <div
                    className="cluster-marker"
                    style={{
                      width: `${30 + (pointCount / points.length) * 20}px`,
                      height: `${30 + (pointCount / points.length) * 20}px`,
                    }}
                    onClick={() => {
                      const expansionZoom = Math.min(
                        supercluster.getClusterExpansionZoom(cluster.id as number),
                        20
                      );

                      setViewState({
                        ...viewState,
                        latitude,
                        longitude,
                        zoom: expansionZoom,
                        transitionDuration: 500
                      });
                    }}
                  >
                    {pointCount}
                  </div>
                </Marker>
              );
            }

            const house = cluster.properties as House;
            
            return (
              <Marker
                key={`house-${house.id}`}
                latitude={latitude}
                longitude={longitude}
                anchor="bottom"
                onClick={e => {
                  e.originalEvent.stopPropagation();
                  handleHouseClick(house);
                }}
              >
                <div className="marker cursor-pointer" title={house.address}>
                  <MapPin className="h-6 w-6 text-red-500" />
                </div>
              </Marker>
            );
          })}

          {selectedHouse && (
            <Popup
              latitude={selectedHouse.latitude}
              longitude={selectedHouse.longitude}
              anchor="bottom"
              onClose={handlePopupClose}
              closeButton={true}
              closeOnClick={false}
              className="house-popup"
            >
              <div className="p-2">
                <h3 className="font-semibold mb-1">{selectedHouse.address}</h3>
                {selectedHouse.rating !== undefined && (
                  <div className="flex items-center mb-1">
                    <Star className="h-4 w-4 text-yellow-500 fill-yellow-500 mr-1" />
                    <span>{selectedHouse.rating.toFixed(1)}</span>
                    {selectedHouse.reviews_count !== undefined && (
                      <span className="text-sm text-gray-500 ml-1">
                        ({selectedHouse.reviews_count} отзывов)
                      </span>
                    )}
                  </div>
                )}
                <button
                  onClick={handleViewHouse}
                  className="w-full mt-2 px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
                >
                  Подробнее
                </button>
              </div>
            </Popup>
          )}
        </Map>

        {/* Map overlay styles for clusters */}
        <style jsx="true">{`
          .cluster-marker {
            background: #1e88e5;
            border-radius: 50%;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 14px;
            cursor: pointer;
            border: 2px solid white;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
          }
          
          .marker {
            transform-origin: bottom;
            transition: transform 0.2s;
          }
          
          .marker:hover {
            transform: scale(1.2);
          }
        `}</style>

        {isLoading && (
          <div className="absolute inset-0 bg-white bg-opacity-70 flex items-center justify-center">
            <div className="bg-white p-4 rounded-lg shadow-md flex items-center">
              <Loader2 className="animate-spin text-blue-500 mr-3" size={24} />
              <span className="text-gray-800">Загрузка домов...</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MapPage;