using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Microsoft.Identity.Web.Resource;

namespace API.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class WeatherForecastController : ControllerBase
    {
        private readonly ILogger<WeatherForecastController> _logger;
        private readonly IConfiguration configuration;

        public WeatherForecastController(ILogger<WeatherForecastController> logger, IConfiguration config)
        {
            _logger = logger;
            configuration = config;
        }

        
        [HttpGet]
        [Authorize(Policy="AllowedAccess")]
        public async Task<string> Get(string city)
        {
            var context = this.HttpContext;
            var url = $"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={configuration["WeatherApiKey"]}";
            var client = new HttpClient();
            var response = await client.GetStringAsync(url);

            return response;
        }
    }
}